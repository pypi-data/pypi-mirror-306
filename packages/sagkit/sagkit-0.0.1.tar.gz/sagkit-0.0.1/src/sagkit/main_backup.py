
do_merging = True
do_spliting = False

import sys, time, random
from typing import List

random.seed(1)

class Job:
    def __init__(self, id:int, BCAT:int, WCAT:int, BCET:int, WCET:int, DDL:int, priority:int, ET_ratio:int) -> None:
        self.id = id
        self.BCAT = BCAT
        self.WCAT = WCAT
        self.BCET = BCET
        self.BCET_REC = BCET
        self.WCET = WCET
        self.WCET_REC = WCET
        self.DDL = DDL
        self.priority = priority
        self.is_ET = 0 if random.randint(0, 99) < 100-ET_ratio else 1
        if not do_spliting and self.is_ET:
            self.BCET = 0
            self.BCET_REC = 0
        
    def set_to_non_triggered(self) -> None:
        self.BCET = 0
        self.WCET = 0
        
    def set_to_triggered(self) -> None:
        self.BCET = self.BCET_REC
        self.WCET = self.WCET_REC
        
    def is_priority_eligible(self, future_jobs:List, time:int) -> bool:
        for future_job in future_jobs:
            if (future_job.WCAT <= time) and (future_job.priority < self.priority):
                return False
        return True
    
    def is_potentially_next(self, future_jobs:List, time:int, state_LFT:int) -> bool:
        if self.BCAT <= state_LFT:
            return True
        for future_job in future_jobs:
            if (future_job.WCAT < time) and (future_job.id != self.id) \
                and future_job.is_priority_eligible(future_jobs, max(future_job.WCAT, state_LFT)):
                return False
        return True

class State:
    def __init__(self, id:int, EFT:int, LFT:int, job_path:List) -> None:
        self.id = id
        self.EFT = EFT
        self.LFT = LFT
        self.depth = len(job_path)
        self.job_path = job_path
        self.next_jobs = []
        self.next_states = []
        
    def is_leaf(self) -> bool:
        return len(self.next_states) == 0
    
        
def edf_scheduler(a:Job, b:Job) -> int:
    if a.DDL < b.DDL:
        return -1
    elif a.DDL > b.DDL:
        return 1
    else:
        if a.priority < b.priority:
            return -1
        elif a.priority > b.priority:
            return 1
        else:
            sys.exit('Same DDL and same priority!')
            
ET_ratio_list = [15]
U_list = [45, 50, 55, 60, 65, 70, 75]
spliting_condition_list = [False, True]

for ET_ratio in ET_ratio_list:
    for U in U_list:
        runnable_number = 1000

        BCAT_list = []
        WCAT_list = []
        BCET_list = []
        WCET_list = []
        DDL_list = []
        priority_list = []
        ET_list = []

        for i in range(runnable_number):
            ET_list.append(0 if random.randint(0, 99) < 100-ET_ratio else 1)
            BCAT = random.randint(1, 9900)
            BCAT_list.append(BCAT)
            WCAT_list.append(BCAT + random.randint(0, 9))
            # BCAT_list.append(0 if ET_list[-1] == 1 else BCAT)
            # WCAT_list.append(0 if ET_list[-1] == 1 else BCAT + random.randint(0, 9))
            BCET = random.randint(2, int(U/5-7))
            BCET_list.append(BCET)
            WCET_list.append(BCET + random.randint(1, 4))
            DDL_list.append(10000)
            priority_list.append(random.randint(1, 10))

        with open("generate_result.txt","w") as dot_file:
            for i in range(runnable_number):
                dot_file.write(str(BCAT_list[i]) + ' ' + str(WCAT_list[i]) + ' ' + str(BCET_list[i]) + ' ' + str(WCET_list[i]) + \
                    ' ' + str(DDL_list[i]) + ' ' + str(priority_list[i]) + ' ' + str(ET_list[i]) + '\n')
        print("Generate input file successfully!")
        print("U = ", sum(WCET_list)/10000)
        
        
        for do_spliting in spliting_condition_list:
            print('ET_ratio:', ET_ratio, 'do_spliting:', do_spliting)
            
            start_time = time.time()
        
            # Read jobs from file
            job_list = []
            # input_file = open('./input/HQYRealTimeJobs_2.txt', 'r')
            input_file = open('./generate_result.txt', 'r')
            for job in input_file:
                job = job.split()
                job_list.append(Job(len(job_list), int(job[0]), int(job[1]), int(job[2]), int(job[3]), int(job[4]), int(job[5]), ET_ratio))
            input_file.close()

            # ET_es_counter = 1
            # non_ET_es_counter = 1
            # for job in job_list:
            #     ET_es_counter *= (job.WCAT - job.BCAT + 1) * (job.WCET - job.BCET + 2) if job.is_ET else (job.WCAT - job.BCAT + 1) * (job.WCET - job.BCET + 1)
            #     non_ET_es_counter *= (job.WCAT - job.BCAT + 1) * (job.WCET + 1) if job.is_ET else (job.WCAT - job.BCAT + 1) * (job.WCET - job.BCET + 1)
            # print('Number of execution scenarios:', ET_es_counter)
            # print('Number of non-ET execution scenarios:', non_ET_es_counter)
            # print('Valid ratio of non-ET SAG:', ET_es_counter/non_ET_es_counter)

            # Initialize root state
            state_list = []
            SAG_root =  State(len(state_list), 0, 0, [])
            state_list.append(SAG_root)

            # find the shortest leaf
            def find_shortest_leaf() -> State:
                leaves = []
                for state in state_list:
                    if state.is_leaf():
                        leaves.append(state)
                shortest_leaf = min(leaves, key=lambda x: x.depth)
                return shortest_leaf

            # Match two states
            def match(a:State, b:State) -> bool:
                if a.depth != b.depth:
                    return False
                return (max(a.EFT, b.EFT) <= min(a.LFT, b.LFT) and sorted(a.job_path, key=lambda s: s.id) == sorted(b.job_path, key=lambda s: s.id))

            # Expansion phase with or without merging
            def expand(leaf:State, job:Job, do_merge:bool) -> None:
                EFT = max(leaf.EFT, job.BCAT) + job.BCET
                future_jobs = [j for j in job_list if j not in leaf.job_path]
                t_H = sys.maxsize
                for future_job in future_jobs:
                    if future_job.priority < job.priority:
                        t_H = min(future_job.WCAT-1, t_H)
                # LFT = min(max(leaf.LFT, job.WCAT), t_H) + job.WCET
                LFT = min(max(leaf.LFT, min(job.WCAT for job in future_jobs)), t_H) + job.WCET
                successor_state = State(len(state_list), EFT, LFT, leaf.job_path + [job])   
                # print('State No.', len(state_list))
                leaf.next_jobs.append(job)
                if do_merge:
                    for state in state_list:
                        if match(state, successor_state):
                            # if leaf.next_states.count(state) == 0:
                            leaf.next_states.append(state)
                            state.EFT = min(state.EFT, successor_state.EFT)
                            state.LFT = max(state.LFT, successor_state.LFT)
                            return
                state_list.append(successor_state)
                leaf.next_states.append(successor_state)


            # construct SAG
            shortest_leaf = SAG_root
            while shortest_leaf.depth < len(job_list):
                eligible_successors = []
                future_jobs = [j for j in job_list if j not in shortest_leaf.job_path]
                for future_job in future_jobs:
                    t_E = max(shortest_leaf.EFT, future_job.BCAT)
                    if future_job.is_priority_eligible(future_jobs, t_E) \
                        and future_job.is_potentially_next(future_jobs, t_E, shortest_leaf.LFT):
                            eligible_successors.append(future_job)
                if len(eligible_successors) == 0:
                    sys.exit('No eligible successor found during construction!')
                for eligible_successor in eligible_successors:
                    expand(leaf=shortest_leaf, job=eligible_successor, do_merge=do_merging)
                    
                    if do_spliting and eligible_successor.is_ET:
                        eligible_successor.set_to_non_triggered()
                        expand(leaf=shortest_leaf, job=eligible_successor, do_merge=True)
                        eligible_successor.set_to_triggered()
                                
                shortest_leaf = find_shortest_leaf()
                

            print('Execution time:', time.time()-start_time, 's')

            # Output SAG as a dot file
            with open("dot.txt","w") as dot_file:
                dot_file.write('digraph finite_state_machine {\n'+
                'rankdir = LR;\n'+
                'size = "8,5";\n'+
                'node [shape = doublecircle];\n'+
                '"S0\\n[0, 0]";\n'+
                'node [shape = circle];\n')
                for state in state_list:
                    for i in range(len(state.next_jobs)):
                        dot_file.write('"S' + str(state.id) + '\\n[' + str(state.EFT) + ', ' + str(state.LFT) + ']" -> "S' + str(state.next_states[i].id) + \
                            '\\n[' + str(state.next_states[i].EFT) + ', ' + str(state.next_states[i].LFT) + ']" [label="J' + str(state.next_jobs[i].id) + '"];\n')
                dot_file.write('}')
                
                
            # Print SAG statistics
            # for state in state_list:
            #     print('State' + str(state.id) + '[' + str(state.EFT), str(state.LFT) + ']')
            #     for i in range(len(state.next_jobs)):
            #         print('    S' + str(state.id) + ' -- J' + str(state.next_jobs[i].id) + ' -> S' + str(state.next_states[i].id))
            print('Number of states:', len(state_list))
            # print('Number of edges:', sum(len(state.next_states) for state in state_list))
            # leaves = []
            # for state in state_list:
            #     if state.is_leaf():
            #         leaves.append(state)
            # print('Minimum Depth:', min(state.depth for state in leaves))
            # width_recorder = [0 for _ in range(len(state_list)+1)]
            # for state in state_list:
            #     width_recorder[state.depth+1] += len(state.next_states)
            # print('Maximum Width:', max(width_recorder))
            # print('Execution time:', time.time()-start_time, 's')