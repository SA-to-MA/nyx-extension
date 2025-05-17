(define (problem instance_4)
	(:domain PolyCraft)

	(:objects
        (:private
		    a1 a2 a3 a4 a5 - agent
		)
	)

	(:init (agent_free a1) (agent_free a2) (agent_free a3) (agent_free a4) (agent_free a5) (= (trees_in_map) 15)
		; Items
		(= (count_log_in_inventory) 0)
		(= (count_planks_in_inventory) 0)
		(= (count_stick_in_inventory) 0)
		(= (count_sack_polyisoprene_pellets_in_inventory) 0)
		(= (count_tree_tap_in_inventory) 0)
		(= (count_pogo_stick) 0)
	)
	(:goal
		(and (= (count_pogo_stick) 5)
		)
	)
)