(define (domain ma-car)
  (:requirements :typing :fluents :time :negative-preconditions)

  (:types car - object)

  (:predicates
    (running ?c - car)
    (engineblown ?c - car)
    (goal_reached ?c - car)
    (transmission_fine ?c - car)
  )

  (:functions
    (d ?c - car)
    (v ?c - car)
    (a ?c - car)
    (up_limit ?c - car)
    (down_limit ?c - car)
    (running_time ?c - car)
  )

  (:action accelerate-accelerate
    :parameters (?c1 ?c2 - car)
    :precondition (and
      (running ?c1)
      (< (a ?c1) (up_limit ?c1))
      (running ?c2)
      (< (a ?c2) (up_limit ?c2))
    )
    :effect (and
      (increase (a ?c1) 1)
      (increase (a ?c2) 1)
    )
  )

  (:action accelerate-decelerate
    :parameters (?c1 ?c2 - car)
    :precondition (and
      (running ?c1)
      (< (a ?c1) (up_limit ?c1))
      (running ?c2)
      (> (a ?c2) (down_limit ?c2))
    )
    :effect (and
      (increase (a ?c1) 1)
      (decrease (a ?c2) 1)
    )
  )

  (:action accelerate-stop
    :parameters (?c - car)
    :precondition (and
      (running ?c)
      (< (a ?c) (up_limit ?c))
      (= (v ?c) 0)
      (>= (d ?c) 30)
      (not (engineblown ?c))
    )
    :effect (and
      (increase (a ?c) 1)
      (goal_reached ?c)
    )
  )

  (:action decelerate-accelerate
    :parameters (?c1 ?c2 - car)
    :precondition (and
      (running ?c1)
      (> (a ?c1) (down_limit ?c1))
      (running ?c2)
      (< (a ?c2) (up_limit ?c2))
    )
    :effect (and
      (decrease (a ?c1) 1)
      (increase (a ?c2) 1)
    )
  )

  (:action decelerate-decelerate
    :parameters (?c1 ?c2 - car)
    :precondition (and
      (running ?c1)
      (> (a ?c1) (down_limit ?c1))
      (running ?c2)
      (> (a ?c2) (down_limit ?c2))
    )
    :effect (and
      (decrease (a ?c1) 1)
      (decrease (a ?c2) 1)
    )
  )

  (:action decelerate-stop
    :parameters (?c - car)
    :precondition (and
      (running ?c)
      (> (a ?c) (down_limit ?c))
      (= (v ?c) 0)
      (>= (d ?c) 30)
      (not (engineblown ?c))
    )
    :effect (and
      (decrease (a ?c) 1)
      (goal_reached ?c)
    )
  )

  (:action stop-accelerate
    :parameters (?c - car)
    :precondition (and
      (= (v ?c) 0)
      (>= (d ?c) 30)
      (not (engineblown ?c))
    )
    :effect (and
      (goal_reached ?c)
      (increase (a ?c) 1)
    )
  )

  (:action stop-decelerate
    :parameters (?c - car)
    :precondition (and
      (= (v ?c) 0)
      (>= (d ?c) 30)
      (not (engineblown ?c))
    )
    :effect (and
      (goal_reached ?c)
      (decrease (a ?c) 1)
    )
  )

  (:action stop-stop
    :parameters (?c - car)
    :precondition (and
      (= (v ?c) 0)
      (>= (d ?c) 30)
      (not (engineblown ?c))
    )
    :effect (and
      (goal_reached ?c)
    )
  )

  (:process moving
    :parameters (?c - car)
    :precondition (and
      (running ?c)
    )
    :effect (and
      (increase (v ?c) (* #t (a ?c)))
      (increase (d ?c) (* #t (v ?c)))
      (increase (running_time ?c) (* #t 1))
    )
  )

  (:action accelerate-noop
    :parameters (?c - car)
    :precondition (and
      (running ?c)
      (not (= (a ?c) (up_limit ?c)))
    )
    :effect ()
  )

  (:action decelerate-noop
    :parameters (?c - car)
    :precondition (and
      (running ?c)
      (not (= (a ?c) (down_limit ?c)))
    )
    :effect ()
  )

  (:action stop-noop
    :parameters (?c - car)
    :precondition (and
      (running ?c)
      (not (= (v ?c) 0))
      (>= (d ?c) 30)
      (not (engineblown ?c))
    )
    :effect ()
  )

  (:process windresistance
    :parameters (?c - car)
    :precondition (and
      (running ?c)
      (>= (v ?c) 50)
    )
    :effect (and
      (decrease (v ?c) (* #t (* 0.1 (* (- (v ?c) 50) (- (v ?c) 50))))))
  )

  (:event engineexplode
    :parameters (?c - car)
    :precondition (and
      (running ?c)
      (>= (a ?c) 1)
      (>= (v ?c) 100)
    )
    :effect (and
      (not (running ?c))
      (engineblown ?c)
      (assign (a ?c) 0)
    )
  )
)
