(define (domain car-ma)
  (:requirements :typing :fluents :time :negative-preconditions)
  (:predicates
    (car1_running)
    (car2_running)
    (car1_engineblown)
    (car2_engineblown)
    (car1_transmission_fine)
    (car2_transmission_fine)
    (car1_goal_reached)
    (car2_goal_reached)
  )
  (:functions
    (car1_d)
    (car2_d)
    (car1_v)
    (car2_v)
    (car1_a)
    (car2_a)
    (car1_up_limit)
    (car2_up_limit)
    (car1_down_limit)
    (car2_down_limit)
    (car1_running_time)
    (car2_running_time)
  )
  (:action car1_accelerate-car2_accelerate
    :precondition (and
      (car1_running)
      (< (car1_a) car1_up_limit)
      (car2_running)
      (< (car2_a) car2_up_limit)
    )
    :effect (and
      (increase (car1_a) 1)
      (increase (car2_a) 1)
    )
  )
  (:action car1_accelerate-car2_decelerate
    :precondition (and
      (car1_running)
      (< (car1_a) car1_up_limit)
      (car2_running)
      (> (car2_a) car2_down_limit)
    )
    :effect (and
      (increase (car1_a) 1)
      (decrease (car2_a) 1)
    )
  )
  (:action car1_accelerate-car2_stop
    :precondition (and
      (car1_running)
      (< (car1_a) car1_up_limit)
      (= (car2_v) car2_0)
      (>= (car2_d) car2_3)
      (not (car2_engineblown))
    )
    :effect (and
      (increase (car1_a) 1)
      (car2_goal_reached)
    )
  )
  (:action car1_decelerate-car2_accelerate
    :precondition (and
      (car1_running)
      (> (car1_a) car1_down_limit)
      (car2_running)
      (< (car2_a) car2_up_limit)
    )
    :effect (and
      (decrease (car1_a) 1)
      (increase (car2_a) 1)
    )
  )
  (:action car1_decelerate-car2_decelerate
    :precondition (and
      (car1_running)
      (> (car1_a) car1_down_limit)
      (car2_running)
      (> (car2_a) car2_down_limit)
    )
    :effect (and
      (decrease (car1_a) 1)
      (decrease (car2_a) 1)
    )
  )
  (:action car1_decelerate-car2_stop
    :precondition (and
      (car1_running)
      (> (car1_a) car1_down_limit)
      (= (car2_v) car2_0)
      (>= (car2_d) car2_3)
      (not (car2_engineblown))
    )
    :effect (and
      (decrease (car1_a) 1)
      (car2_goal_reached)
    )
  )
  (:action car1_stop-car2_accelerate
    :precondition (and
      (= (car1_v) car1_0)
      (>= (car1_d) car1_3)
      (not (car1_engineblown))
      (car2_running)
      (< (car2_a) car2_up_limit)
    )
    :effect (and
      (car1_goal_reached)
      (increase (car2_a) 1)
    )
  )
  (:action car1_stop-car2_decelerate
    :precondition (and
      (= (car1_v) car1_0)
      (>= (car1_d) car1_3)
      (not (car1_engineblown))
      (car2_running)
      (> (car2_a) car2_down_limit)
    )
    :effect (and
      (car1_goal_reached)
      (decrease (car2_a) 1)
    )
  )
  (:action car1_stop-car2_stop
    :precondition (and
      (= (car1_v) car1_0)
      (>= (car1_d) car1_3)
      (not (car1_engineblown))
      (= (car2_v) car2_0)
      (>= (car2_d) car2_3)
      (not (car2_engineblown))
    )
    :effect (and
      (car1_goal_reached)
      (car2_goal_reached)
    )
  )
  (:process car1_moving
    :precondition (and
      (car1_running)
    )
    :effect (and
      (increase (car1_v) (* #t car1_a))
      (increase (car1_d) (* #t car1_v))
      (increase (car1_running_time) (* #t 1))
    )
  )
  (:process car1_windresistance
    :precondition (and
      (car1_running)
      (>= (car1_v) car1_5)
    )
    :effect (and
      (decrease (car1_v) (* #t (* 0.1 (* (- car1_v 50) (- car1_v 50)))))
    )
  )
  (:process car2_moving
    :precondition (and
      (car2_running)
    )
    :effect (and
      (increase (car2_v) (* #t car2_a))
      (increase (car2_d) (* #t car2_v))
      (increase (car2_running_time) (* #t 1))
    )
  )
  (:process car2_windresistance
    :precondition (and
      (car2_running)
      (>= (car2_v) car2_5)
    )
    :effect (and
      (decrease (car2_v) (* #t (* 0.1 (* (- car2_v 50) (- car2_v 50)))))
    )
  )
  (:event car1_engineexplode
    :precondition (and
      (car1_running)
      (>= (car1_a) car1_1)
      (>= (car1_v) car1_1)
    )
    :effect (and
      (not (car1_running))
      (car1_engineblown)
      (assign (car1_a) 0)
    )
  )
  (:event car2_engineexplode
    :precondition (and
      (car2_running)
      (>= (car2_a) car2_1)
      (>= (car2_v) car2_1)
    )
    :effect (and
      (not (car2_running))
      (car2_engineblown)
      (assign (car2_a) 0)
    )
  )
)
