(define (problem blocks-4-0 )
(:domain blocks )
(:objects a1 - agent
a2 - agent
a - block
c - block
b - block
d - block
)
(:init (handempty a2 )(handempty a1 )(clear c )(clear d )(clear a )(ontable b )(ontable c )(ontable d )(on a b )(dif_agent a1 a2 )(dif_agent a2 a1 )(dif_block a c )(dif_block a b )(dif_block a d )(dif_block c a )(dif_block c b )(dif_block c d )(dif_block b a )(dif_block b c )(dif_block b d )(dif_block d a )(dif_block d c )(dif_block d b ))
(:goal (and (on b a )(on c b )(on d c )))
)