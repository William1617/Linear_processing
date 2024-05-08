import numpy as np

def get_next(A,cur_id,type):
    At=A.copy()
    At[cur_id[0]][cur_id[1]]=0
    # for row
    if(type%2==1):
        ava_ids=np.argwhere(At[cur_id[0]]>0)
    
        if(len(ava_ids)<=cur_id[2]):
            return []
        else:
            return [cur_id[0],ava_ids[cur_id[2]][0],0]
    #for colomn
    else: 
        ava_ids=np.argwhere(At[:,cur_id[1]]>0)

        if(len(ava_ids)<=cur_id[2]):
            return []
        else:
            return [ava_ids[cur_id[2]][0],cur_id[1],0]


def test_optimal(A,cost):
    m,n=np.shape(A)
    u=np.zeros(m)
    v=np.zeros(n)
    # u0=0
    rows=[0]
    cols=[]
    while(len(rows)<m or len(cols)<n):
        for id1 in rows:
            for id2 in range(n):
                if(A[id1][id2]>0 and id2 not in cols):
                    v[id2]=cost[id1][id2]-u[id1]
                    cols.append(id2)
        for id2 in cols:
            for id1 in range(m):
                if(A[id1][id2]>0 and id1 not in rows):
                    u[id1]=cost[id1][id2]-v[id2]
                    rows.append(id1)
  
    test_mat=np.zeros_like(cost)
    is_optima=True
    
    for id1 in range(m):
        for id2 in range(n):
            if(A[id1][id2]==0):
                test_mat[id1][id2]=cost[id1][id2]-u[id1]-v[id2]
                if(test_mat[id1][id2]<0):
                    is_optima=False
                    break
    
    min_idx=np.argmin(test_mat)
    start_id=[min_idx//n,min_idx%n,0]
    min_value=np.min(test_mat)
    return is_optima,start_id,min_value

def find_loop(A,start_id):
    loops=[]
    loops.append(start_id)
    type=0
    next_id=get_next(A,loops[-1],type)
    type =(type+1)%2
    loops[-1][2] +=1
    loops.append(next_id)
    
    while(len(loops)>0)  :
        next_id=get_next(A,loops[-1],type)
        # one for clomn one for row
        type =(type+1)%2
        loops[-1][2] +=1
        
       
        while(len(next_id)==0 and len(loops)>0):
            # no loop finded
            if(len(loops)==1):
                return loops
            
            loops=loops[:-1]
            next_id=get_next(A,loops[-1],type)
            
            type =(type+1)%2
            loops[-1][2] +=1
        if(type==1 and next_id[0]==start_id[0]):
            loops.append(next_id)
            return loops 
        if(type==0 and next_id[1]==start_id[1]):
            loops.append(next_id)
            return loops 
            
        loops.append(next_id)

    return loops
        
            

def transportation(cost,supply,demand):
    assert np.sum(supply)>=np.sum(demand)
    A=np.zeros_like(cost)
    newcost=cost.copy()
    new_supply=supply.copy()
    new_demand=demand.copy()

    cost_max=np.max(newcost)
    count =0
    
    while(np.mean(newcost)<cost_max+1 ):
        max_diff=np.argmax(np.sort(newcost,0)[1]-np.sort(newcost,0)[0])
        max_diffvalue=np.max(np.sort(newcost,0)[1]-np.sort(newcost,0)[0])
     
        if(max_diffvalue==0):
            for idx in range(len(demand)):
                
                if(np.mean(newcost[:,idx])<cost_max+1):
                    max_diff=idx
                    break
           
        max_row=np.argmin(newcost[:,max_diff])
        if(new_supply[max_row]>=new_demand[max_diff]):
            A[max_row][max_diff]=new_demand[max_diff]
            # add mask
            newcost[:,max_diff]=cost_max +1
            
            new_supply[max_row]=new_supply[max_row]-new_demand[max_diff]
            new_demand[max_diff]=0
        if(new_supply[max_row]<=new_demand[max_diff]):
            # for the new new_supply[max_row]==new_demand[max_diff]
            if(new_supply[max_row]>0):
                A[max_row][max_diff]=new_supply[max_row]
            newcost[max_row,:]=cost_max +1
            
            new_demand[max_diff]=new_demand[max_diff]-new_supply[max_row]
            new_supply[max_row]=0
       
        
   
    is_optimal,stat_id,min_value=test_optimal(A,cost)
    while(is_optimal==False):
        loops=find_loop(A,stat_id)
        # no loop finded
        if(len(loops)<4):
            return A
        for idx in range(len(loops)):
            if(idx%2==0):
                A[loops[idx][0]][loops[idx][1]] -=min_value
            else:
                A[loops[idx][0]][loops[idx][1]] +=min_value
        
        is_optimal,stat_id,min_value=test_optimal(A,cost)
    print(A)
    return A



if __name__=='__main__':
    supply=[10,15,25]
    demand=[8,20,12,10]
    cost=np.zeros((3,4))
    cost[0][0]=12
    cost[0][1]=5
    cost[0][2]=7
    cost[0][3]=5
    cost[1][0]=6
    cost[1][1]=5
    cost[1][2]=7
    cost[1][3]=6
    cost[2][0]=10
    cost[2][1]=2
    cost[2][2]=6
    cost[2][3]=1
    A=transportation(cost,supply,demand)
    totcost=np.sum(A*cost)
    print(totcost)
