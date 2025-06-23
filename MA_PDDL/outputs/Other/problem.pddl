(define (problem pb-collab )
(:domain push-box )
(:objects agent1 - agent
agent2 - agent
agent3 - agent
box1 - box
)
(:init (= (box-pos box1 )0 )(= (push-power agent1 )0.3 )(= (push-power agent2 )0.4 )(= (push-power agent3 )0.8 )(dif_agent agent1 agent2 )(dif_agent agent1 agent3 )(dif_agent agent2 agent1 )(dif_agent agent2 agent3 )(dif_agent agent3 agent1 )(dif_agent agent3 agent2 ))
(:goal (>= (box-pos box1 )10 ))
)