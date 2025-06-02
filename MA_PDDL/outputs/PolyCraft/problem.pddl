(define (problem instance_2 )
(:domain polycraft )
(:objects a1 - agent
a2 - agent
)
(:init (= (plan_cost )0 )(= (turn a2 )2 )(= (turn a1 )1 )(= (cur_turn )1 )(agent_free a1 )(agent_free a2 )(= (trees_in_map )10 )(= (count_log_in_inventory )0 )(= (count_planks_in_inventory )0 )(= (count_stick_in_inventory )0 )(= (count_sack_polyisoprene_pellets_in_inventory )0 )(= (count_tree_tap_in_inventory )0 )(= (count_pogo_stick )0 )(dif_agent a1 a2 )(dif_agent a2 a1 ))
(:goal (and (= (count_pogo_stick )2 )))
(:metric minimize (plan_cost ))
)