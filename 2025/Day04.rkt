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

; convert list of strings to 2D array, wuth 0 and 1s
; pad it twith 0s rows and cols
(define diagram
  (λ (ls)
    (define (prepare ls)
      (list*->array
       (for/list ([line ls])
         (for/list ([element (string->list line)])
           (if (char=? element #\@) 1 0))) number?)) ; convert to 0 and 1
    (array-append* (list
                    (array 0) ; pad cols
                    (array-append* (list
                                    (array 0) ; pad rows
                                    (prepare ls)
                                    (array 0)))
                    (array 0)) 1))) 

; selects array 3x3 around x y of arr
(define (pick-3 arr x y)
  (let* ([row-from (sub1 y)]
         [row-to (+ 2 y)]
         [col-from (sub1 x)]
         [col-to (+ 2 x)]
         [rows (in-range row-from row-to)]
         [cols (in-range col-from col-to)]
         [range (list rows cols)])
    (array-slice-ref arr range)))  ; (row col)

(define (count inp)
  (let* ([arr (diagram inp)]
         [size (sub1 (vector-ref (array-shape arr) 0))])
    (for/sum ([col (in-range 1 size)])
      (for/sum ([row (in-range 1 size)])
        (if (zero? (array-count positive? (array-slice-ref arr (list col row))))
            0
            (if (> 5 (array-all-sum (pick-3 arr row col)))
                1
                0))))))
             
(display "Part 1: ")         
(if (= 13 (count test-input))
    (count input)
    (error "wrong result"))
