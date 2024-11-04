from .utils import *
from .main import *

def preprocessing(fen, elo_self, elo_oppo, elo_dict, all_moves_dict):
        
    if fen.split(' ')[1] == 'w':
        board = chess.Board(fen)
    elif fen.split(' ')[1] == 'b':
        board = chess.Board(fen).mirror()
    else:
        raise ValueError(f"Invalid fen: {fen}")
        
    board_input = board_to_tensor(board)
    
    elo_self = map_to_category(elo_self, elo_dict)
    elo_oppo = map_to_category(elo_oppo, elo_dict)
    
    legal_moves = torch.zeros(len(all_moves_dict))
    legal_moves_idx = torch.tensor([all_moves_dict[move.uci()] for move in board.legal_moves])
    legal_moves[legal_moves_idx] = 1
    
    return board_input, elo_self, elo_oppo, legal_moves


class TestDataset(torch.utils.data.Dataset):
    
    def __init__(self, data, all_moves_dict, elo_dict):
        
        self.all_moves_dict = all_moves_dict
        self.data = data.values.tolist()
        self.elo_dict = elo_dict
    
    def __len__(self):
        
        return len(self.data)
    
    def __getitem__(self, idx):
        
        fen, _, elo_self, elo_oppo = self.data[idx]

        board_input, elo_self, elo_oppo, legal_moves = preprocessing(fen, elo_self, elo_oppo, self.elo_dict, self.all_moves_dict)
        
        return fen, board_input, elo_self, elo_oppo, legal_moves


def get_preds(model, dataloader, all_moves_dict_reversed):
    
    all_probs = []
    predicted_move_probs = []
    predicted_moves = []
    predicted_win_probs = []
    
    device = next(model.parameters()).device
    
    model.eval()
    with torch.no_grad():
        
        for fens, boards, elos_self, elos_oppo, legal_moves in dataloader:
            
            boards = boards.to(device)
            elos_self = elos_self.to(device)
            elos_oppo = elos_oppo.to(device)
            legal_moves = legal_moves.to(device)

            logits_maia, _, logits_value = model(boards, elos_self, elos_oppo)
            logits_maia_legal = logits_maia * legal_moves
            probs = logits_maia_legal.softmax(dim=-1)

            all_probs.append(probs.cpu())
            predicted_move_probs.append(probs.max(dim=-1).values.cpu())
            predicted_move_indices = probs.argmax(dim=-1)
            for i in range(len(fens)):
                fen = fens[i]
                predicted_move = all_moves_dict_reversed[predicted_move_indices[i].item()]
                if fen.split(' ')[1] == 'b':
                    predicted_move = mirror_move(predicted_move)
                predicted_moves.append(predicted_move)

            predicted_win_probs.append((logits_value / 2 + 0.5).cpu())
            predicted_win_probs = [min(max(0, x), 1) for x in predicted_win_probs]
    
    all_probs = torch.cat(all_probs).cpu().numpy()
    predicted_move_probs = torch.cat(predicted_move_probs).numpy()
    predicted_win_probs = torch.cat(predicted_win_probs).numpy()
    
    return all_probs, predicted_move_probs, predicted_moves, predicted_win_probs


def inference_batch(data, model, verbose, batch_size, num_workers):

    all_moves = get_all_possible_moves()
    all_moves_dict = {move: i for i, move in enumerate(all_moves)}
    elo_dict = create_elo_dict()
    
    all_moves_dict_reversed = {v: k for k, v in all_moves_dict.items()}
    dataset = TestDataset(data, all_moves_dict, elo_dict)
    dataloader = torch.utils.data.DataLoader(dataset, 
                                            batch_size=batch_size, 
                                            shuffle=False, 
                                            drop_last=False,
                                            num_workers=num_workers)
    if verbose:
        dataloader = tqdm.tqdm(dataloader)
        
    all_probs, predicted_move_probs, predicted_moves, predicted_win_probs = get_preds(model, dataloader, all_moves_dict_reversed)
    
    data['predicted_move'] = predicted_moves
    data['predicted_move_prob'] = predicted_move_probs
    data['predicted_win_prob'] = predicted_win_probs
    data['all_probs'] = all_probs.tolist()
    
    acc = (data['predicted_move'] == data['move']).mean()
    
    return data, round(acc, 4)


def prepare():

    all_moves = get_all_possible_moves()
    all_moves_dict = {move: i for i, move in enumerate(all_moves)}
    elo_dict = create_elo_dict()
    
    all_moves_dict_reversed = {v: k for k, v in all_moves_dict.items()}
    
    return [all_moves_dict, elo_dict, all_moves_dict_reversed]


def inference_each(model, prepared, fen, elo_self, elo_oppo):
    
    all_moves_dict, elo_dict, all_moves_dict_reversed = prepared
    
    board_input, elo_self, elo_oppo, legal_moves = preprocessing(fen, elo_self, elo_oppo, elo_dict, all_moves_dict)
    
    device = next(model.parameters()).device
    
    model.eval()
    
    board_input = board_input.unsqueeze(dim=0).to(device)
    elo_self = torch.tensor([elo_self]).to(device)
    elo_oppo = torch.tensor([elo_oppo]).to(device)
    legal_moves = legal_moves.unsqueeze(dim=0).to(device)
    
    logits_maia, _, logits_value = model(board_input, elo_self, elo_oppo)
    logits_maia_legal = logits_maia * legal_moves
    probs = logits_maia_legal.softmax(dim=-1)

    predicted_move_probs = probs.max(dim=-1).values.item()
    predicted_move_index = probs.argmax(dim=-1)
    predicted_move = all_moves_dict_reversed[predicted_move_index.item()]
    if fen.split(' ')[1] == 'b':
        predicted_move = mirror_move(predicted_move)
    predicted_win_prob = (logits_value / 2 + 0.5).item()
    predicted_win_prob = min(max(0, predicted_win_prob), 1)
    
    return {"predicted_move": predicted_move, "predicted_move_prob": round(predicted_move_probs, 4), "predicted_win_prob": round(predicted_win_prob, 4)}

