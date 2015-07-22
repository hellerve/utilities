:-lib(branch_and_bound).
:-lib(fd).
:-lib(fd_global).
:-lib(lists).

balance(P, W, BL, BU) :- balance(P, W, BL, BU, 0).

balance(P, W, BL, BU, D):-
  P::BL..BU,

  length(P, N),
  fillwith(D, N, ZL),

  0#=P*W,

  fd:disjunctive(P,ZL,_),

  labeling(P).

absSum(A, B) :- absSum(A, 0, B).

absSum([], Sum, Sum).
absSum([H|T], X, Sum) :-
  M #= X + abs(H),
  absSum(T, M, Sum).

test([A, B, C]) :-
  absSum([1, 2, 3], 6),
  balance([A, B, C], [30, 40, 50], -5, 5).

fillwith(D, X, L) :- fillwith(D, X, L, []).

fillwith(D, 0, L, L).
fillwith(D, N, L, Acc) :-
  M is N - 1,
  append(Acc, [D], Nacc),
  fillwith(D, M, L, Nacc).
