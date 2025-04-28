(define (problem multi-car-problem )
(:domain car )
(:requirements :typing :fluents :time )
(:objects car1 - agent
car2 - agent
car3 - agent
)
(:init (running car1 )(transmission_fine car1 )(= (running_time car1 )0 )(= (d car1 )0 )(= (v car1 )0 )(= (a car1 )0 )(= (up_limit car1 )10 )(= (down_limit car1 )-1 )(running car2 )(transmission_fine car2 )(= (running_time car2 )0 )(= (d car2 )0 )(= (v car2 )0 )(= (a car2 )0 )(= (up_limit car2 )12 )(= (down_limit car2 )-2 )(running car3 )(transmission_fine car3 )(= (running_time car3 )0 )(= (d car3 )0 )(= (v car3 )0 )(= (a car3 )0 )(= (up_limit car3 )12 )(= (down_limit car3 )-2 )(dif_agent car1 car2 )(dif_agent car1 car3 )(dif_agent car2 car1 )(dif_agent car2 car3 )(dif_agent car3 car1 )(dif_agent car3 car2 ))
(:goal (and (goal_reached car1 )(not (engineblown car1 ))(<= (running_time car1 )50 )(transmission_fine car1 )(goal_reached car2 )(not (engineblown car2 ))(<= (running_time car2 )50 )(transmission_fine car2 )(goal_reached car3 )(not (engineblown car3 ))(<= (running_time car3 )50 )(transmission_fine car3 )))
)