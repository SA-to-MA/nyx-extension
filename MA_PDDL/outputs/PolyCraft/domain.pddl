(define (domain polycraft)
(:requirements :strips :typing :negative-preconditions :fluents )
(:types agent - object )
(:predicates (agent_free ?agent - agent )(agent_get_log ?agent - agent )(agent_craft_plank ?agent - agent )(agent_craft_stick ?agent - agent )(agent_get_sack ?agent - agent )(agent_place_tree_tap ?agent - agent )(agent_craft_pogo_stick ?agent - agent )(dif_agent ?ob1 - agent ?ob2 - agent ))
(:functions (trees_in_map )(count_log_in_inventory )(count_planks_in_inventory )(count_stick_in_inventory )(count_sack_polyisoprene_pellets_in_inventory )(count_tree_tap_in_inventory )(count_pogo_stick ))
(:action return_stick
:parameters (?a1 - agent)
:precondition (and
(agent_craft_stick ?a1 )
)
:effect (and
(agent_free ?a1 )
(not (agent_craft_stick ?a1 ))
(increase (count_stick_in_inventory )4 )
)
)
(:action return_sack
:parameters (?a1 - agent)
:precondition (and
(agent_get_sack ?a1 )
)
:effect (and
(agent_free ?a1 )
(not (agent_get_sack ?a1 ))
(increase (count_sack_polyisoprene_pellets_in_inventory )1 )
)
)
(:action craft_wooden_pogo
:parameters (?a1 - agent)
:precondition (and
(>= (count_planks_in_inventory )2 )
(>= (count_stick_in_inventory )4 )
(>= (count_sack_polyisoprene_pellets_in_inventory )1 )
(agent_free ?a1 )
)
:effect (and
(decrease (count_planks_in_inventory )2 )
(decrease (count_stick_in_inventory )4 )
(decrease (count_sack_polyisoprene_pellets_in_inventory )1 )
(not (agent_free ?a1 ))
(agent_craft_pogo_stick ?a1 )
)
)
(:action return_wooden_pogo
:parameters (?a1 - agent)
:precondition (and
(agent_craft_pogo_stick ?a1 )
)
:effect (and
(agent_free ?a1 )
(not (agent_craft_pogo_stick ?a1 ))
(increase (count_pogo_stick )1 )
)
)
(:action return_log
:parameters (?a1 - agent)
:precondition (and
(agent_get_log ?a1 )
)
:effect (and
(agent_free ?a1 )
(not (agent_get_log ?a1 ))
(increase (count_log_in_inventory )1 )
)
)
(:action craft_plank
:parameters (?a1 - agent)
:precondition (and
(>= (count_log_in_inventory )1 )
(agent_free ?a1 )
)
:effect (and
(decrease (count_log_in_inventory )1 )
(not (agent_free ?a1 ))
(agent_craft_plank ?a1 )
)
)
(:action craft_tree_tap
:parameters (?a1 - agent)
:precondition (and
(>= (count_planks_in_inventory )5 )
(>= (count_stick_in_inventory )1 )
(agent_free ?a1 )
)
:effect (and
(decrease (count_planks_in_inventory )5 )
(decrease (count_stick_in_inventory )1 )
(not (agent_free ?a1 ))
(agent_place_tree_tap ?a1 )
)
)
(:action place_tree_tap
:parameters (?a1 - agent)
:precondition (and
(>= (trees_in_map )1 )
(>= (count_tree_tap_in_inventory )1 )
(agent_free ?a1 )
)
:effect (and
(not (agent_free ?a1 ))
(agent_get_sack ?a1 )
)
)
(:action craft_stick
:parameters (?a1 - agent)
:precondition (and
(>= (count_planks_in_inventory )2 )
(agent_free ?a1 )
)
:effect (and
(decrease (count_planks_in_inventory )2 )
(not (agent_free ?a1 ))
(agent_craft_stick ?a1 )
)
)
(:action return_tree_tap
:parameters (?a1 - agent)
:precondition (and
(agent_place_tree_tap ?a1 )
)
:effect (and
(agent_free ?a1 )
(not (agent_place_tree_tap ?a1 ))
(increase (count_tree_tap_in_inventory )1 )
)
)
(:action return_plank
:parameters (?a1 - agent)
:precondition (and
(agent_craft_plank ?a1 )
)
:effect (and
(agent_free ?a1 )
(not (agent_craft_plank ?a1 ))
(increase (count_planks_in_inventory )4 )
)
)
(:action get_log
:parameters (?a1 - agent)
:precondition (and
(>= (trees_in_map )1 )
(agent_free ?a1 )
)
:effect (and
(decrease (trees_in_map )1 )
(not (agent_free ?a1 ))
(agent_get_log ?a1 )
)
)
)
