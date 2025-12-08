#lang racket

(require math/array)
(require 2htdp/batch-io)

(define test-input (list
                    "..@@.@@@@."
                    "@@@.@.@.@@"
                    "@@@@@.@.@@"
                    "@.@@@@..@."
                    "@@.@@@@.@@"
                    ".@@@@@@@.@"
                    ".@.@.@.@@@"
                    "@.@@@.@@@@"
                    ".@@@@@@@@."
                    "@.@.@@@.@."))

(define input (read-lines "Day04_input.txt"))

; convert list of strings to 2D array, with 0 and 1s
(define diagram
  (λ (ls)
    (list*->array
     (for/list ([line ls])
       (for/list ([element (string->list line)])
         (if (char=? element #\@) 1 0))) number?))) ; convert to 0 and 1
    
; selects array 3x3 (in most cases) around x y of arr
(define (pick-3 arr x y)
  (let* ([size (vector-ref (array-shape arr) 0)] ; array is square, no need to check other axle
         [clamp  ; make sure 3x3 is not going outside array area.
          (λ (a) (cond
            [(> a size) size]
            [(negative? a) 0]
            [else a]))]
         [row-from (clamp (sub1 y))] 
         [row-to (clamp (+ 2 y))]
         [col-from (clamp (sub1 x))]
         [col-to (clamp (+ 2 x))]
         [rows (in-range row-from row-to)]
         [cols (in-range col-from col-to)]
         [range (list rows cols)])
    (array-slice-ref arr range)))  ; (rows cols)

(define (count inp)
  (let* ([arr (diagram inp)]
         [size (vector-ref (array-shape arr) 0)]
         [processed-lists (for/list ([col (in-range 0 size)])
                            (for/list ([row (in-range 0 size)])
                              (if (zero? (array-count positive? (array-slice-ref arr (list col row))))
                                  0
                                  (if (> 5 (array-count positive? (pick-3 arr row col)))
                                      1
                                      0))))])

    (for/sum ([ln processed-lists])
      (for/sum ([element ln]) element))))
    
(define (count-2 inp)
  (let* ([arr (diagram inp)]
         [size (vector-ref (array-shape arr) 0)])
    (define (remove-rolls arr removed)
      (define processed-lists
        (for/list ([col (in-range 0 size)])
          (for/list ([row (in-range 0 size)])
            (if (zero? (array-count positive? (array-slice-ref arr (list col row))))
                0
                (if (> 5 (array-count positive? (pick-3 arr row col)))
                    1
                    2)))))
      (define result 
        ; return pair (count of removed rolls . array with new layout)
        (cons (for/sum ([ln processed-lists])
                (foldl + 0 (filter odd? ln)))
              (list*->array (for/list ([ln processed-lists])
                              (for/list ([element ln])
                                (cond
                                  [(= element 2) 1]
                                  [(= element 1) 0]
                                  [else element]))) number?)))
      (if (zero? (car result))
          removed
          (remove-rolls (cdr result) (+ removed (car result)))))
    (remove-rolls arr 0)))

(display "Part 1: ")         
(if (= 13 (count test-input))
    (count input)
    (error "wrong result"))

(display "Part 2: ")         
(if (= 43 (count-2 test-input))
    (count-2 input)
    (error "wrong result"))

