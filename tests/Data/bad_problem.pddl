(define (problem blocks-test) (:domain blocks)
(:objects
    a - block
    b - block
    c - block
(:init
    (ontable a)
    (clear a)
    (handempty a1)
)
(:goal
    (on b a)
)
