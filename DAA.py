import math

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.subordinates = []

def build_tree(structure, root_name):
    nodes = {}
    for boss, reports in structure.items():
        nodes.setdefault(boss, TreeNode(boss))
        for r in reports:
            nodes.setdefault(r, TreeNode(r))
            nodes[boss].subordinates.append(nodes[r])
    return nodes[root_name]

def get_comms_team(root):
    
    if not root:
        return []
        
    dp = {}            
    best_sub_state2 = {} 
    
    def dfs(u):
        
        if not u.subordinates:
            dp[u] = [1, 0, float('inf')]
            return
            
        
        for v in u.subordinates:
            dfs(v)
            
        
        inf_count = 0
        sum_state2 = 0
        for v in u.subordinates:
            if dp[v][2] == float('inf'):
                inf_count += 1
            else:
                sum_state2 += dp[v][2]
                
        
        dp_u_0 = 1
        for v in u.subordinates:
            dp_u_0 += min(dp[v][0], dp[v][1])
            
        
        if inf_count == 0:
            dp_u_1 = sum_state2
        else:
            dp_u_1 = float('inf')
            
        
        dp_u_2 = float('inf')
        best_w = None
        
        for w in u.subordinates:
            if inf_count == 0:
                cost = sum_state2 - dp[w][2] + dp[w][0]
                if cost < dp_u_2:
                    dp_u_2 = cost
                    best_w = w
            elif inf_count == 1 and dp[w][2] == float('inf'):
                cost = sum_state2 + dp[w][0]
                if cost < dp_u_2:
                    dp_u_2 = cost
                    best_w = w
                    
        dp[u] = [dp_u_0, dp_u_1, dp_u_2]
        best_sub_state2[u] = best_w

    
    dfs(root)
    
    team_members = set()
    
    
    def reconstruct(u, state):
        if state == 0:
            team_members.add(u.val)
            for v in u.subordinates:
                if dp[v][0] <= dp[v][1]:
                    reconstruct(v, 0)
                else:
                    reconstruct(v, 1)
        elif state == 1:
            for v in u.subordinates:
                reconstruct(v, 2)
        elif state == 2:
            w = best_sub_state2[u]
            if w:
                reconstruct(w, 0)
                for v in u.subordinates:
                    if v != w:
                        reconstruct(v, 2)
                        
    
    if dp[root][0] <= dp[root][2]:
        reconstruct(root, 0)
    else:
        reconstruct(root, 2)
        
    return list(team_members)


