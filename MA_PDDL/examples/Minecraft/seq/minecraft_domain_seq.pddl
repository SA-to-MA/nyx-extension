; PolyCraft basic domain

(define (domain PolyCraft)

    (:requirements :strips :typing :negative-preconditions :fluents)

    (:types
        agent - object
    )

    (:predicates
        (agent_free ?agent - agent)
        (agent_get_log ?agent - agent)
        (agent_craft_plank ?agent - agent)
        (agent_craft_stick ?agent - agent)
        (agent_get_sack ?agent - agent)
        (agent_place_tree_tap ?agent - agent)
        (agent_craft_pogo_stick ?agent - agent)

    )

    (:functions
        ; Map
        (trees_in_map)

        ; Items
        (count_log_in_inventory)
        (count_planks_in_inventory)
        (count_stick_in_inventory)
        (count_sack_polyisoprene_pellets_in_inventory)
        (count_tree_tap_in_inventory)
        (count_pogo_stick)
    )

    ; Actions
    (:action GET_LOG
        :parameters (?a - agent)
        :precondition (and
            (>= (trees_in_map) 1)
            (agent_free ?a)
        )
        :effect (and
            (decrease (trees_in_map) 1)
            (not (agent_free ?a))
            (agent_get_log ?a)
        )
    )

    (:action RETURN_LOG
        :parameters (?a - agent)
        :precondition (and
            (agent_get_log ?a)
        )
        :effect (and
            (agent_free ?a)
            (not (agent_get_log ?a))
            (increase (count_log_in_inventory) 1)
        )
    )

    (:action CRAFT_PLANK
        :parameters (?a - agent)
        :precondition (and
            (>= (count_log_in_inventory) 1)
            (agent_free ?a)
        )
        :effect (and
            (decrease (count_log_in_inventory) 1)
            (not (agent_free ?a))
            (agent_craft_plank ?a)
        )
    )

    (:action RETURN_PLANK
        :parameters (?a - agent)
        :precondition (and
            (agent_craft_plank ?a)
        )
        :effect (and
            (agent_free ?a)
            (not (agent_craft_plank ?a))
            (increase (count_planks_in_inventory) 4)
        )
    )

    (:action CRAFT_STICK
        :parameters (?a - agent)
        :precondition (and
            (>= (count_planks_in_inventory) 2)
            (agent_free ?a)
        )
        :effect (and
            (decrease (count_planks_in_inventory) 2)
            (not (agent_free ?a))
            (agent_craft_stick ?a)
        )
    )

    (:action RETURN_STICK
        :parameters (?a - agent)
        :precondition (and
            (agent_craft_stick ?a)
        )
        :effect (and
            (agent_free ?a)
            (not (agent_craft_stick ?a))
            (increase (count_stick_in_inventory) 4)
        )
    )

    (:action CRAFT_TREE_TAP
        :parameters (?a - agent)
        :precondition (and
            (>= (count_planks_in_inventory) 5)
            (>= (count_stick_in_inventory) 1)
            (agent_free ?a)
        )
        :effect (and
            (decrease (count_planks_in_inventory) 5)
            (decrease (count_stick_in_inventory) 1)
            (not (agent_free ?a))
            (agent_place_tree_tap ?a)
        )
    )

    (:action RETURN_TREE_TAP
        :parameters (?a - agent)
        :precondition (and
            (agent_place_tree_tap ?a)
        )
        :effect (and
            (agent_free ?a)
            (not (agent_place_tree_tap ?a))
            (increase (count_tree_tap_in_inventory) 1)
        )
    )

    (:action CRAFT_WOODEN_POGO
        :parameters (?a - agent)
        :precondition (and
            (>= (count_planks_in_inventory) 2)
            (>= (count_stick_in_inventory) 4)
            (>= (count_sack_polyisoprene_pellets_in_inventory) 1)
            (agent_free ?a)
        )
        :effect (and
            (decrease (count_planks_in_inventory) 2)
            (decrease (count_stick_in_inventory) 4)
            (decrease
                (count_sack_polyisoprene_pellets_in_inventory)
                1)
            (not (agent_free ?a))
            (agent_craft_pogo_stick ?a)
        )
    )

    (:action RETURN_WOODEN_POGO
        :parameters (?a - agent)
        :precondition (and
            (agent_craft_pogo_stick ?a)
        )
        :effect (and
            (agent_free ?a)
            (not (agent_craft_pogo_stick ?a))
            (increase (count_pogo_stick) 1)
        )
    )

    (:action PLACE_TREE_TAP
        :parameters (?a - agent)
        :precondition (and
            (>= (trees_in_map) 1)
            (>= (count_tree_tap_in_inventory) 1)
            (agent_free ?a)
        )
        :effect (and
            (not (agent_free ?a))
            (agent_get_sack ?a)
        )
    )

    (:action RETURN_SACK
        :parameters (?a - agent)
        :precondition (and
            (agent_get_sack ?a)
        )
        :effect (and
            (agent_free ?a)
            (not (agent_get_sack ?a))
            (increase
                (count_sack_polyisoprene_pellets_in_inventory)
                1)
        )
    )

)