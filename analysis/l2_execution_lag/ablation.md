--- none (= T9 baseline): latency=0.0, observation_offset=0.0  (trigger step 21)
    [meta-cand] (item_4) cost=50 feasible=True conflicts=981 min_dist=15.37233196754729
    [meta-cand] (item_2) cost=61 feasible=True conflicts=982 min_dist=22.68288481907288
    [meta] step=21 trigger=theta_crossed winner=deliver_item(item_4) queue=["deliver_item(item_2)"]
--- latency only: latency=1.0, observation_offset=0.0  (trigger step 21)
    [meta-cand] (item_4) cost=54 feasible=True conflicts=989 min_dist=15.37233196754729
    [meta-cand] (item_2) cost=65 feasible=True conflicts=1070 min_dist=22.68288481907288
    [meta] step=21 trigger=theta_crossed winner=deliver_item(item_4) queue=["deliver_item(item_2)"]
--- offset only: latency=0.0, observation_offset=1.0  (trigger step 21)
    [meta-cand] (item_4) cost=50 feasible=False conflicts=941 min_dist=0.49296688528208676
    [meta-cand] (item_2) cost=61 feasible=True conflicts=982 min_dist=9.43749337532574
    [meta] step=21 trigger=theta_crossed winner=deliver_item(item_2) queue=["deliver_item(item_4)"]
--- both (= HEAD): latency=1.0, observation_offset=1.0  (trigger step 21)
    [meta-cand] (item_4) cost=54 feasible=False conflicts=949 min_dist=0.49296688528208676
    [meta-cand] (item_2) cost=65 feasible=True conflicts=1070 min_dist=9.43749337532574
    [meta] step=21 trigger=theta_crossed winner=deliver_item(item_2) queue=["deliver_item(item_4)"]
