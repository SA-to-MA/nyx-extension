(define (problem blocks-problem)
  (:domain blocks)
  (:objects
    a b c d e
    (:private a1 a2 - agent)
  )
  (:init
    (ontable a)
    (ontable b)
    (clear a)
    (clear b)
    (handempty a1)
  )
  (:goal
    (on a b)
  )
)
