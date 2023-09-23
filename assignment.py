import numpy as np

def test_optimal(cost):
    m,_=np.shape(cost)
    
    ids=[]
    ava_ids=np.argwhere(cost[0]==0)
   
    ids.append(ava_ids[0][0])
    while(len(ids)>0 and len(ids)<m ):
        cur_row=len(ids)
        ava_ids=np.argwhere(cost[cur_row]==0)
        
        find_next=False
        for id2 in range(len(ava_ids)):
            if(ava_ids[id2][0] not in ids):
                ids.append(ava_ids[id2][0])
                find_next=True
                break
        # go back
     
        while(find_next==False):
        
            pre_ids=np.argwhere(cost[len(ids)-1]==0)
            while(ids[-1]>= max(pre_ids)[0]):
                # not optimal
                if(len(ids)==1):
                    return ids
                ids=ids[:-1]
        
                pre_ids=np.argwhere(cost[len(ids)-1]==0)
            
            ava_ids=np.argwhere(cost[len(ids)-1]==0)
            #print(ava_ids)
            for id2 in range(len(ava_ids)):
                if(ava_ids[id2][0] not in ids and ava_ids[id2][0]>ids[-1]):
                    ids[-1]=ava_ids[id2][0]
                    find_next=True
                    break
            if(find_next==False):
                if(len(ids)==1):
                    return ids
                ids=ids[:-1]
    
            
    return ids
            
def assignment(cost):
    m,n=np.shape(cost)
    assert m>=n
    newcost=np.zeros((m,m))
    newcost[:,:n]=cost
    newcost=(newcost.T-np.min(newcost,1)).T
    
    newcost=newcost-np.min(newcost,0)
    ids=test_optimal(newcost)
    
    mask=newcost.copy()
    max_value=np.max(newcost)+1
    if(m>n):
        mask[:,n:] +=max_value
    while(len(ids)<m):
        for id1 in range(m):
            for id2 in range(m):
                if(mask[id1][id2]<max_value and newcost[id1][id2]==0):
                # cover as much as zero as possible
                    row_num=len(np.argwhere(newcost[id1]==0))-len(np.argwhere((mask[id1]%max_value)==0))
                    col_num=len(np.argwhere(newcost[:,id2]==0))-len(np.argwhere((mask[:,id2]%max_value)==0))
                    if(row_num>col_num):
                        mask[id1] +=max_value
                    if(row_num<col_num):
                        mask[:,id2] +=max_value
                    if(row_num==col_num):
                        if(len(np.argwhere(newcost[id1]==0))>len(np.argwhere(newcost[:,id2]==0))):
                            mask[id1] +=max_value
                        else:
                            mask[:,id2] +=max_value
        min_value=np.min(mask)
        for id1 in range(m):
            for id2 in range(n):
                if(mask[id1][id2]>=2*max_value):
                    newcost[id1][id2] +=min_value
                if(mask[id1][id2]<max_value):
                    newcost[id1][id2] -=min_value
        ids=test_optimal(newcost)
    
    return ids
                



if __name__=='__main__':
  
    cost=np.zeros((5,4))
    cost[0][0]=27
    cost[0][1]=23
    cost[0][2]=22
    cost[0][3]=24
    cost[1][0]=68
    cost[1][1]=27
    cost[1][2]=21
    cost[1][3]=26
    cost[2][0]=58
    cost[2][1]=26
    cost[2][2]=44
    cost[2][3]=25
    cost[3][0]=27
    cost[3][1]=55
    cost[3][2]=21
    cost[3][3]=24
    cost[4][0]=5
    cost[4][1]=3
    cost[4][2]=23
    cost[4][3]=26
   
    ids=assignment(cost)
    tot_cost=0
    m,n=np.shape(cost)
    for idx in range(len(ids)):
        if(ids[idx]<n):
            tot_cost+=cost[idx][ids[idx]]
    print(tot_cost)
    
   
  