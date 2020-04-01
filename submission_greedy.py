def greedy_agent_twostep(observation, configuration):
    feasible_actions = [c for c in range(configuration.columns) if observation.board[c] == 0]
    reward = [-1e4]*configuration.columns 
    for i in feasible_actions:
        reward[i] = evaluate_action_twostep(observation.board, i, configuration.columns, observation.mark, configuration.inarow)
    action = int(range(0, configuration.columns)[np.argmax(reward)])
    return action
def greedy_agent_twostep(observation, configuration):
    feasible_actions = [c for c in range(configuration.columns) if observation.board[c] == 0]
    reward = [-1e4]*configuration.columns 
    for i in feasible_actions:
        reward[i] = evaluate_action_twostep(observation.board, i, configuration.columns, observation.mark, configuration.inarow)
    action = int(range(0, configuration.columns)[np.argmax(reward)])
    return action
def submit_greedy_agent_twostep(observation, configuration):
    
    import numpy as np

    def board_to_matrix(board, columns):
        return np.reshape(np.array(board), (int(len(board)/columns), columns))

    def get_longest_chain(vector, mark):
        logic_vector = np.equal(vector, mark)
        count = 0 
        result = 0 
        for i in range(logic_vector.shape[0]):
            if logic_vector[i]:
                count+= 1   
                result = max(result, count)  
            else:
                count = 0
          
    return max(result, count)

    def manipulate_board(board, column, columns, mark):
        is_zero_board = np.equal(board, 0)
        relevant_vector = is_zero_board[column::columns]
        relevant_row = np.max(np.nonzero(relevant_vector))    
    
        manipulated_board = np.copy(board)
        manipulated_board[relevant_row*columns + column] = mark 
        return(manipulated_board)

    def evaluate_action_onestep(board, column, columns, mark):
    
        manipulated_board = manipulate_board(board, column, columns, mark) 
    
        # Compute ALL diagnoal longest_chain values
        a = board_to_matrix(manipulated_board, columns)
        diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
        diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
        value_diagonal = 0
        for diag in diags:
            value_diagonal = max(get_longest_chain(diag, mark), value_diagonal)
    
        # Compute horizontal and vertical longest chains (lazy eval)
        values_vertical = np.apply_along_axis(get_longest_chain, 1, a, mark) # vertical
        values_horizontal = np.apply_along_axis(get_longest_chain, 0, a, mark) # horizontal
        max_value = max(np.append(values_vertical, values_horizontal))
    
        return(max(value_diagonal, max_value))
        
    def evaluate_action_twostep(board, column, columns, mark, inarow):
    
        # Initialize index of opponent
        if mark==1:
            anti_mark = 2
        else:
            anti_mark = 1
        
        manipulated_board = manipulate_board(board, column, columns, mark) 
        a = board_to_matrix(manipulated_board, columns)
        value = evaluate_action_onestep(board, column, columns, mark)
        goal_status = value/inarow
    
        if goal_status == 1:
            reward = 1
        else: 
            # check for loss-possibility
            feasible_anti_actions = [j for j in range(columns) if manipulated_board[j] == 0]
            anti_value = []
            for j in feasible_anti_actions:
                anti_value.append(evaluate_action_onestep(manipulated_board, j, columns, anti_mark))
            if max(anti_value) >=inarow:
                reward = -1e2
            else:
                reward = value - max(anti_value)
            
        return reward
     
    feasible_actions = [c for c in range(configuration.columns) if observation.board[c] == 0]
    reward = [-1e4]*configuration.columns 
    for i in feasible_actions:
        reward[i] = evaluate_action_twostep(observation.board, i, configuration.columns, observation.mark, configuration.inarow)
    action = int(range(0, configuration.columns)[np.argmax(reward)])
    
    return action
def submit_greedy_agent_twostep(observation, configuration):
    
    import numpy as np

    def board_to_matrix(board, columns):
        return np.reshape(np.array(board), (int(len(board)/columns), columns))

    def get_longest_chain(vector, mark):
        logic_vector = np.equal(vector, mark)
        count = 0 
        result = 0 
        for i in range(logic_vector.shape[0]):
            if logic_vector[i]:
                count+= 1   
                result = max(result, count)  
            else:
                count = 0
          
    return max(result, count)

    def manipulate_board(board, column, columns, mark):
        is_zero_board = np.equal(board, 0)
        relevant_vector = is_zero_board[column::columns]
        relevant_row = np.max(np.nonzero(relevant_vector))    
    
        manipulated_board = np.copy(board)
        manipulated_board[relevant_row*columns + column] = mark 
        return(manipulated_board)

    def evaluate_action_onestep(board, column, columns, mark):
    
        manipulated_board = manipulate_board(board, column, columns, mark) 
    
        # Compute ALL diagnoal longest_chain values
        a = board_to_matrix(manipulated_board, columns)
        diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
        diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
        value_diagonal = 0
        for diag in diags:
            value_diagonal = max(get_longest_chain(diag, mark), value_diagonal)
    
        # Compute horizontal and vertical longest chains (lazy eval)
        values_vertical = np.apply_along_axis(get_longest_chain, 1, a, mark) # vertical
        values_horizontal = np.apply_along_axis(get_longest_chain, 0, a, mark) # horizontal
        max_value = max(np.append(values_vertical, values_horizontal))
    
        return(max(value_diagonal, max_value))
        
    def evaluate_action_twostep(board, column, columns, mark, inarow):
    
        # Initialize index of opponent
        if mark==1:
            anti_mark = 2
        else:
            anti_mark = 1
        
        manipulated_board = manipulate_board(board, column, columns, mark) 
        a = board_to_matrix(manipulated_board, columns)
        value = evaluate_action_onestep(board, column, columns, mark)
        goal_status = value/inarow
    
        if goal_status == 1:
            reward = 1
        else: 
            # check for loss-possibility
            feasible_anti_actions = [j for j in range(columns) if manipulated_board[j] == 0]
            anti_value = []
            for j in feasible_anti_actions:
                anti_value.append(evaluate_action_onestep(manipulated_board, j, columns, anti_mark))
            if max(anti_value) >=inarow:
                reward = -1e2
            else:
                reward = value - max(anti_value)
            
        return reward
     
    feasible_actions = [c for c in range(configuration.columns) if observation.board[c] == 0]
    reward = [-1e4]*configuration.columns 
    for i in feasible_actions:
        reward[i] = evaluate_action_twostep(observation.board, i, configuration.columns, observation.mark, configuration.inarow)
    action = int(range(0, configuration.columns)[np.argmax(reward)])
    
    return action
def submit_greedy_agent_twostep(observation, configuration):
    
    import numpy as np

    def board_to_matrix(board, columns):
        return np.reshape(np.array(board), (int(len(board)/columns), columns))

    def get_longest_chain(vector, mark):
        logic_vector = np.equal(vector, mark)
        count = 0 
        result = 0 
        for i in range(logic_vector.shape[0]):
            if logic_vector[i]:
                count+= 1   
                result = max(result, count)  
            else:
                count = 0
          
        return max(result, count)

    def manipulate_board(board, column, columns, mark):
        is_zero_board = np.equal(board, 0)
        relevant_vector = is_zero_board[column::columns]
        relevant_row = np.max(np.nonzero(relevant_vector))    
    
        manipulated_board = np.copy(board)
        manipulated_board[relevant_row*columns + column] = mark 
        return(manipulated_board)

    def evaluate_action_onestep(board, column, columns, mark):
    
        manipulated_board = manipulate_board(board, column, columns, mark) 
    
        # Compute ALL diagnoal longest_chain values
        a = board_to_matrix(manipulated_board, columns)
        diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
        diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
        value_diagonal = 0
        for diag in diags:
            value_diagonal = max(get_longest_chain(diag, mark), value_diagonal)
    
        # Compute horizontal and vertical longest chains (lazy eval)
        values_vertical = np.apply_along_axis(get_longest_chain, 1, a, mark) # vertical
        values_horizontal = np.apply_along_axis(get_longest_chain, 0, a, mark) # horizontal
        max_value = max(np.append(values_vertical, values_horizontal))
    
        return(max(value_diagonal, max_value))
        
    def evaluate_action_twostep(board, column, columns, mark, inarow):
    
        # Initialize index of opponent
        if mark==1:
            anti_mark = 2
        else:
            anti_mark = 1
        
        manipulated_board = manipulate_board(board, column, columns, mark) 
        a = board_to_matrix(manipulated_board, columns)
        value = evaluate_action_onestep(board, column, columns, mark)
        goal_status = value/inarow
    
        if goal_status == 1:
            reward = 1
        else: 
            # check for loss-possibility
            feasible_anti_actions = [j for j in range(columns) if manipulated_board[j] == 0]
            anti_value = []
            for j in feasible_anti_actions:
                anti_value.append(evaluate_action_onestep(manipulated_board, j, columns, anti_mark))
            if max(anti_value) >=inarow:
                reward = -1e2
            else:
                reward = value - max(anti_value)
            
        return reward
     
    feasible_actions = [c for c in range(configuration.columns) if observation.board[c] == 0]
    reward = [-1e4]*configuration.columns 
    for i in feasible_actions:
        reward[i] = evaluate_action_twostep(observation.board, i, configuration.columns, observation.mark, configuration.inarow)
    action = int(range(0, configuration.columns)[np.argmax(reward)])
    
    return action
