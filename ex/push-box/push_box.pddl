(define (domain push-box)
  (:requirements :typing :fluents :continuous-effects :time :negative-preconditions)
  (:types agent box)

  (:predicates
    (pushing ?a - agent ?b - box)
  )

  (:functions
    (box-pos ?b - box)
    (push-power ?a - agent)
  )

  (:action start-push
    :parameters (?a - agent ?b - box)
    :precondition (not (pushing ?a ?b))
    :effect (pushing ?a ?b)
  )

  (:action stop-push
    :parameters (?a - agent ?b - box)
    :precondition (pushing ?a ?b)
    :effect (not (pushing ?a ?b))
  )

  (:process move-box
    :parameters (?a - agent ?b - box)
    :precondition (pushing ?a ?b)
    :effect (increase (box-pos ?b) (* #t (push-power ?a)))
  )
)
