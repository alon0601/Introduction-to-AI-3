# Introduction-to-AI-3
הוראות הפעלה: The input test should be in the following format:

#X 1                ; Maximum x coordinate
#Y 1                ; Maximum y coordinate
#B 0 0 1 0          ; Edge from (0,0) to (1,0) is always blocked
#F 1 0 1 1 0.8      ; Edge from (1,0) to (1,1) is fragile, with p = 1-qi = 0.8
#F 0 0 0 1 0.8
#V 1 0 F 0.2    ; Vertex (1,0) probability of package given low demand season 0.2
#V 1 1 F 0.3    ; Vertex (1,1) probability package given low demand  0.3
#L 0.1        ; Global leakage probability 0.1
#S 0.1 0.4 0.5 ; Prior distribution over season: 0.1 for low, 0.4 for medium, 0.5 for high

## How to add new evidence:
In order to add season evidence please enter : season <one of [l,m,h]> (l for low, m for medium and h for high).
example:
season l  ;indicates new evidence where season = low.

In order to add vertex evidence please enter : (<vertex>) <one of [True,False]> (vertex need to be replaced with legal coordinates).
example:
(1,0) True ;indicates that we have a package at (1,0).

In order to add edge evidence please enter : (<edge>) <one of [True,False]> (edge need to be replaced with legal F edge).
example:
((0,0),(1,0)) False ;indicates that the edge ((0,0),(1,0)) is not blocked.

please dont add spare whitespaces.
