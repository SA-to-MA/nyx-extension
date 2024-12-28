(define (problem blocks-4-0 )
(:domain blocks )
(:objects a1 - agent
a2 - agent
a - block
c - block
b - block
)
(:init (handempty a1 )(handempty a2 )(clear c )(clear a )(ontable a )(ontable b )(on c b )(dif a1 a2 )(dif a2 a1 )(dif a c )(dif a b )(dif c a )(dif c b )(dif b a )(dif b c ))
(:goal (and (on c b )(on b a )))
)