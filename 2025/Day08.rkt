#lang racket
(require racket/set data/ddict 2htdp/batch-io rackunit)

(define test-input (list
                    "162,817,812"
                    "57,618,57"
                    "906,360,560"
                    "592,479,940"
                    "352,342,300"
                    "466,668,158"
                    "542,29,236"
                    "431,825,988"
                    "739,650,466"
                    "52,470,668"
                    "216,146,977"
                    "819,987,18"
                    "117,168,530"
                    "805,96,715"
                    "346,949,466"
                    "970,615,88"
                    "941,993,340"
                    "862,61,35"
                    "984,92,344"
                    "425,690,689"))

; distance bewteen 2 juction boxes (as vector)
(define (distance-square a b)
  (let ([ax (vector-ref a 0)]
        [ay (vector-ref a 1)]
        [az (vector-ref a 2)]
        [bx (vector-ref b 0)]
        [by (vector-ref b 1)]
        [bz (vector-ref b 2)])
    
    (+ (expt (- bx ax) 2)
       (expt (- by ay) 2)
       (expt (- bz az) 2))))

;(distance-square (vector 425 690 689) (vector 162 817 812))
;(distance-square (vector 57 618 57) (vector 592 479 940))
         

(define (build-junctions inp)
  (map list->vector
       (for/list ([ls inp])
         (map string->number
              (regexp-split #rx"," ls)))))
    
;(define (distance a b)


; list ((a . b) . distance), sorted by distance a, b = vectors 
(define (junctions-ls test-input)
  (let ([junctions (build-junctions test-input)]
        [visited (mutable-set (cons 0 0))])
    
    (filter (λ (a) (positive? (cdr a))) ; filter out zero distance
            (sort ; sort by distance
             (for*/list ([a junctions]
                         [b junctions])
               (cond
                 [(or (set-member? visited (cons a b))
                      (set-member? visited (cons b a))) (cons 0 0)] ; remove duplicates: a->b b->a
                 [else (set-add! visited (cons a b))
                       (cons (cons b a) (distance-square a b))])) < #:key cdr))))

(define cache (ddict-copy-clear(mutable-ddict (cons (vector 1 2 3) (vector 1 2 3)) -1)))

(define (process-juctions ls)
  (for/list ([l ls]
             [id (in-naturals)]
             #:break (eq? 5 id))
    (let ([a (car (car l))]
          [b (cdr (car l))])
      (displayln (list id cache))
      (cond
        [(and (ddict-has-key? cache a)  ; both vectors in dict
              (ddict-has-key? cache b))
           (let ([common-id (ddict-ref cache a)]
                 [alt-id (ddict-ref cache b)])
             (if (eq? common-id alt-id)
                 (begin
                   (displayln (list a b "part of" common-id))
                   0) ; do nothing, part of the same circuit
                 (for ([(juke circ) (in-dict cache)])  ; scan all dict
                   (if (= alt-id circ) ; find all boxed from old circuit
                       (ddict-set! cache b common-id) ; rename them to new circuit
                       0))))]
        [(ddict-has-key? cache a) (ddict-set! cache b ; add b to dict
                                              (ddict-ref cache a))] ;
        [(ddict-has-key? cache b) (ddict-set! cache a ; add a to dict
                                              (ddict-ref cache b))] ;
        [else (begin
                (ddict-set! cache a id)
                (ddict-set! cache b id))]))))

(process-juctions (junctions-ls test-input))

;(junctions-ls test-input)

cache

