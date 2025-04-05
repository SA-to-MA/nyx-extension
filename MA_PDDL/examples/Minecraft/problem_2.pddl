(define (problem instance_2)
	(:domain PolyCraft)

	(:objects
        (:private
		    a1 a2 - agent
		)
	)

	(:init
		(agent_free a1)
		(agent_free a2)
		(= (trees_in_map) 10)
		; Items
		(= (count_log_in_inventory) 0)
		(= (count_planks_in_inventory) 0)
		(= (count_stick_in_inventory) 0)
		(= (count_sack_polyisoprene_pellets_in_inventory) 0)
		(= (count_tree_tap_in_inventory) 0)
		(= (count_pogo_stick) 0)
	)
	(:goal
		(and (= (count_pogo_stick) 2)
		)
	)
)