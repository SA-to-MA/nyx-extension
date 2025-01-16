(define (problem logistics-8-1) (:domain logistics)
(:objects
	obj21 - package
	obj22 - package
	obj23 - package
	obj33 - package
	obj32 - package
	obj31 - package
	apt3 - airport
	apt2 - airport
	apt1 - airport
	obj11 - package
	obj13 - package
	obj12 - package
	pos2 - location
	pos3 - location
	apn1 - airplane
	tru1 - truck
	cit1 - city
	pos1 - location
	cit2 - city
	tru2 - truck
	tru3 - truck
	cit3 - city
)

(:init
	(at obj22 pos2)
	(at obj12 pos1)
	(at obj11 pos1)
	(at tru1 pos1)
	(in-city tru1 pos1 cit1)
	(at obj33 pos3)
	(at obj32 pos3)
	(at tru3 pos3)
	(at apn1 apt3)
	(in-city tru2 pos2 cit2)
	(in-city tru3 apt3 cit3)
	(in-city tru2 apt2 cit2)
	(at obj21 pos2)
	(at obj13 pos1)
	(in-city tru3 pos3 cit3)
	(at obj31 pos3)
	(at tru2 pos2)
	(at obj23 pos2)
	(in-city tru1 apt1 cit1)
)

(:goal
	(and
	(at obj13 pos2)
	(at obj21 pos3)
	(at obj32 apt2)
	(at obj12 pos3)
	(at obj22 pos3)
	(at obj31 apt1)
	(at obj33 apt3)
	(at obj23 apt2)	
)
)

)