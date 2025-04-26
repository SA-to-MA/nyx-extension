(define (domain blocks)
  (:requirements :typing)
  (:types block agent - object)

  (:predicates
    (on ?x - block ?y - block)
    (ontable ?x - block)
    (clear ?x - block)
    (:private (holding ?a - agent ?x - block) (handempty ?a - agent))
  )
)
