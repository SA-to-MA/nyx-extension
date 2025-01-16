(define (problem elevators-sequencedstrips-p8_8_1) (:domain elevators-sequencedstrips)
(:objects
	p2 - passenger
	p3 - passenger
	p0 - passenger
	p1 - passenger
	p6 - passenger
	p7 - passenger
	p4 - passenger
	p5 - passenger
	n8 - count
	n0 - count
	n1 - count
	n2 - count
	n3 - count
	n4 - count
	n5 - count
	n6 - count
	slow1-0 - slow-elevator
	n7 - count
	slow0-0 - slow-elevator
	fast1 - fast-elevator
	fast0 - fast-elevator
)

(:init
	(next n2 n3)
	(reachable-floor slow0-0 n3)
	(passengers fast1 n0)
	(above n0 n4)
	(passengers fast0 n0)
	(above n2 n6)
	(can-hold slow1-0 n2)
	(above n2 n7)
	(above n6 n8)
	(reachable-floor fast1 n6)
	(reachable-floor slow0-0 n0)
	(above n2 n5)
	(passenger-at p0 n3)
	(lift-at slow0-0 n3)
	(reachable-floor slow1-0 n4)
	(above n0 n1)
	(reachable-floor fast0 n0)
	(above n1 n4)
	(above n0 n8)
	(above n0 n3)
	(above n5 n7)
	(above n4 n8)
	(reachable-floor fast0 n8)
	(above n4 n5)
	(reachable-floor slow1-0 n7)
	(reachable-floor fast1 n4)
	(above n4 n7)
	(lift-at fast0 n6)
	(above n0 n6)
	(next n7 n8)
	(above n7 n8)
	(above n3 n5)
	(above n5 n6)
	(passenger-at p1 n8)
	(reachable-floor fast0 n6)
	(above n1 n5)
	(reachable-floor slow1-0 n5)
	(above n0 n7)
	(above n2 n3)
	(passenger-at p5 n4)
	(can-hold fast0 n1)
	(reachable-floor fast1 n2)
	(lift-at fast1 n2)
	(above n2 n8)
	(above n2 n4)
	(reachable-floor slow0-0 n4)
	(above n5 n8)
	(reachable-floor slow0-0 n2)
	(passenger-at p2 n6)
	(can-hold slow0-0 n2)
	(above n0 n5)
	(above n3 n7)
	(next n3 n4)
	(above n0 n2)
	(above n3 n8)
	(reachable-floor fast0 n4)
	(reachable-floor slow0-0 n1)
	(above n1 n7)
	(above n1 n8)
	(above n1 n2)
	(passengers slow0-0 n0)
	(above n1 n6)
	(next n6 n7)
	(can-hold fast0 n2)
	(passenger-at p7 n8)
	(passengers slow1-0 n0)
	(next n5 n6)
	(can-hold slow1-0 n1)
	(passenger-at p4 n5)
	(above n3 n4)
	(passenger-at p6 n0)
	(above n4 n6)
	(reachable-floor fast1 n8)
	(above n6 n7)
	(reachable-floor fast0 n2)
	(next n4 n5)
	(above n1 n3)
	(can-hold fast1 n2)
	(next n1 n2)
	(above n3 n6)
	(reachable-floor fast1 n0)
	(can-hold fast1 n3)
	(can-hold fast0 n3)
	(reachable-floor slow1-0 n6)
	(can-hold slow0-0 n1)
	(lift-at slow1-0 n8)
	(reachable-floor slow1-0 n8)
	(next n0 n1)
	(can-hold fast1 n1)
	(passenger-at p3 n4)
)

(:goal
	(and
	(passenger-at p0 n1)
	(passenger-at p7 n2)
	(passenger-at p4 n0)
	(passenger-at p5 n6)
	(passenger-at p1 n5)
	(passenger-at p3 n8)
	(passenger-at p2 n3)
	(passenger-at p6 n2)	
)
)

)