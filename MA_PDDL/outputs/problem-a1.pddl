(define (problem blocks-4-0 )
(:domain blocks )
(:objects a1 - agent
a - block
c - block
b - block
)
(:init (handempty a1 )(handempty a2 )(clear c )(clear a )(ontable a )(ontable b )(on c b )(dif_block a c )(dif_block a b )(dif_block c a )(dif_block c b )(dif_block b a )(dif_block b c ))
(:goal (and (on c b )(on b a )))
)