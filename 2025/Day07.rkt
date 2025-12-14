#lang racket
(require racket/set 2htdp/batch-io rackunit)

(define test-input (list
                    ".......S......."
                    "..............."
                    ".......^......."
                    "..............."
                    "......^.^......"
                    "..............."
                    ".....^.^.^....."
                    "..............."
                    "....^.^...^...."
                    "..............."
                    "...^.^...^.^..."
                    "..............."
                    "..^...^.....^.."
                    "..............."
                    ".^.^.^.^.^...^."
                    "..............."))

(define input (read-lines "Day07_input.txt"))

; set of beams. starts with S point with single pair (x . y)
(define (build-beams inp)
  (let ([y 0]
        [x (string-find (car inp) "S")])
  (mutable-set (cons x y))))

; set with all splitters
(define (build-splitters inp)
  (list->set
   (append*
    (filter (negate empty?) ; filter out all rows where there is no splitter
            (for/list ([line inp]
                       [y (in-naturals)])
              (filter pair? ; filter out all voids
                      (for/list ([element line]
                                 [x (in-naturals)])
                        (case element
                          [(eq=? #\^) (cons x y)]))))))))
      
(define (part-1 inp)
  (let ([beams (build-beams inp)]
        [splitters (build-splitters inp)]
        [width (string-length (car inp))]
        [height (length inp)])
    
    (let next-step ([beams beams]
                    [sum 0]
                    [new-beams (set-copy-clear beams)])
    ; iterate all beams and count how many splits happens in single iteration
      (let ([splits-in-iteration
             (for/fold([splits-count 0])
                      ([beam beams])
               (let ([x (car beam)]
                     [y (cdr beam)])
                 (cond
                   [(<= height y) splits-count] ; out of bounds
                   [(set-member? splitters beam) ; beam in splitter position
                    (if (< (add1 x) width) ; check borders, if split posible
                        (set-add! new-beams (cons (add1 x) (add1 y)))
                        0)
                    (if (<= 0 (sub1 x))
                        (set-add! new-beams (cons (sub1 x) (add1 y)))
                        0)
                    (add1 splits-count)]
                 
                   [else (set-add! new-beams (cons x (add1 y))) ; no split, just descent
                         splits-count])))])
        (if (set-empty? new-beams)
            sum  ; no beams? all exited the manifold, show sum
            (next-step new-beams (+ sum splits-in-iteration) (set-copy-clear new-beams)))))))

(check-equal? (part-1 test-input) 21)
(display "Part 1: ")
(part-1 input)
