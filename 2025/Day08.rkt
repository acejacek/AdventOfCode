#lang racket
(require racket/set data/ddict 2htdp/batch-io rackunit)

(define test-input (list
;                    "1,1,1"
;                    "2,953,2"
;                    "3,76,3"
;                    "4,9,9"
;                    "5,79,1"
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
                    "425,690,689"
                    ))

(define input (read-lines "Day08_input.txt"))

; distance^2 bewteen 2 juction boxes (as vector)
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

(define (build-junctions inp)
  (map list->vector
       (remove (list #f) ; cleanup empty line at end of file
               (for/list ([ls inp])
                 (map string->number
                      (regexp-split #rx"," ls))))))

; list ((a . b) . distance), sorted by distance a, b = vectors 
(define (junctions-ls inp)
  (let ([junctions (build-junctions inp)]
        [visited (mutable-set (cons 0 0))])
    
    (filter (λ (vector-pairs) (positive? (cdr vector-pairs))) ; filter out zero distance
            (sort ; sort by distance
             (for*/list ([a junctions]
                         [b junctions])
               (cond
                 [(or (set-member? visited (cons a b))
                      (set-member? visited (cons b a))) (cons 0 0)] ; remove duplicates: a->b b->a
                 [else (set-add! visited (cons a b))
                       (cons (cons a b) (distance-square a b))]))
             < #:key cdr))))

; this process pairs-count of pairs of juntions pairs and returns cache 
(define (process-juctions ls pairs-count)
  (let ([cache (ddict-copy-clear(mutable-ddict (cons (vector 1 2 3) (vector 4 5 6)) -1))])
    (for ([l ls]
          [id (in-naturals)]
          #:break (eq? pairs-count id))  ; process only this number of junction pairs
      (let ([a (caar l)] 
            [b (cdar l)])
        (cond
          [(and (ddict-has-key? cache a)  ; both vectors in dict
                (ddict-has-key? cache b))
           (let ([common-id (ddict-ref cache a)]
                 [alt-id (ddict-ref cache b)])
             (cond ; in same or different circuts?
               [(eq? common-id alt-id) 0] ; do nothing, part of the same circuit
               [else
                (for ([(juke circ) (in-dict cache)])  ; scan all dict
                  (if (= alt-id circ) ; find all boxed from old circuit
                      (ddict-set! cache juke common-id) ; rename them to new circuit
                      0))]))]
          [(ddict-has-key? cache a) (ddict-set! cache b ; add b to dict
                                                (ddict-ref cache a))] ;
          [(ddict-has-key? cache b) (ddict-set! cache a ; add a to dict
                                                (ddict-ref cache b))] ;
          [else (ddict-set! cache a id)
                (ddict-set! cache b id)])))
    cache))

(define (top-3 inp pairs)
  (let* ([junctions (junctions-ls inp)]
         [cache (process-juctions junctions pairs)] ; get cache ready    
         [ids (ddict-values cache)]) ; pull list of values (circuits IDs) frim cache
      
      (apply * ; multiply all by one another
           (for/list ([i (take  ; top 3 
                          (sort ; sort by number of boxes, desc
                           (hash->list 
                            (let ([cache (make-hash)]) ; in cache keep nb of boxes in circuit ID
                              (for ([circuitID ids])
                                (cond
                                  [(hash-has-key? cache circuitID) (hash-update!
                                                                    cache circuitID add1)]
                                  [else (hash-set! cache circuitID 1)]))
                              cache)) ; return cache after "for"
                           #:key cdr >) ; frequence is (CircuitID . freq)
                          3)])
             (cdr i)))))

;(check-equal? (top-3 test-input 10) 40)
;(display "Part 1: ")
;(check-equal? (top-3 input 1000) 62186)
;(top-3 input 1000)
;cache

; this populates cache 
(define (process-juctions-2 inp)
  (let ([final-dist (box 0)]
        [cache (ddict-copy-clear (ddict-copy-clear(mutable-ddict
                                                   (cons (vector 1 2 3) (vector 4 5 6)) -1)))])
    (for ([l (junctions-ls inp)]  ; process list of juctionboxes, ((a . b) . dist), sorted by dist
          [id (in-naturals)])
      #:break (positive? (unbox final-dist))
      (let ([a (caar l)]
            [b (cdar l)])
        (displayln (list a b (cdr l)))
        (if (and (equal? b #(117 168 530))
                 (equal? a #(216 146 977)))
            (set-box! final-dist 1)
            void)
        (cond
          [(and (ddict-has-key? cache a)  ; both vectors in dict (are part of some circuit)
                (ddict-has-key? cache b))
           (let ([common-id (ddict-ref cache a)]
                 [alt-id (ddict-ref cache b)])
             (cond ; in same or different circuts?
               [(eq? common-id alt-id) void] ; do nothing, part of the same circuit
               [else
                (for ([(juke circ) (in-dict cache)])  ; scan all dict
                  (if (= alt-id circ) ; find all boxed from old circuit
                      (ddict-set! cache juke common-id) ; rename them to new circuit
                      void))
                (when (apply = (ddict-values cache)) ; all junction boxex belong to same circuit!
                  (displayln (list "** final pair:" a b))
                  (displayln cache)
;                  (set-box! final-dist (* (vector-ref a 0)
;                                          (vector-ref b 0)))
                  )]))]
                                   
          [(ddict-has-key? cache a) (ddict-set! cache b ; add b to dict
                                                (ddict-ref cache a))] ;
          [(ddict-has-key? cache b) (ddict-set! cache a ; add a to dict
                                                (ddict-ref cache b))] ;
          [else (ddict-set! cache a id)  ; create new, disconnected circuit
                (ddict-set! cache b id)])))
    (displayln cache)
    (unbox final-dist)))

;(junctions-ls test-input)

(process-juctions-2 test-input)
;cache

; 13588916 is too low