(define (problem blocks-4-0 )
(:domain blocks )
(:objects a1 - agent
a2 - agent
a3 - agent
a4 - agent
a - block
c - block
b - block
d - block
e - block
)
(:init (handempty a2 )(handempty a1 )(handempty a3 )(handempty a4 )(clear c )(clear d )(clear e )(ontable b )(ontable c )(ontable d )(on a b )(on e a )(dif_agent a1 a2 )(dif_agent a1 a3 )(dif_agent a1 a4 )(dif_agent a2 a1 )(dif_agent a2 a3 )(dif_agent a2 a4 )(dif_agent a3 a1 )(dif_agent a3 a2 )(dif_agent a3 a4 )(dif_agent a4 a1 )(dif_agent a4 a2 )(dif_agent a4 a3 )(dif_block a c )(dif_block a b )(dif_block a d )(dif_block a e )(dif_block c a )(dif_block c b )(dif_block c d )(dif_block c e )(dif_block b a )(dif_block b c )(dif_block b d )(dif_block b e )(dif_block d a )(dif_block d c )(dif_block d b )(dif_block d e )(dif_block e a )(dif_block e c )(dif_block e b )(dif_block e d ))
(:goal (and (ontable e )(ontable b )(on c b )(on d c )(on a e )))
)