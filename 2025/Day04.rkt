#lang racket

(require math/array)
(require 2htdp/batch-io)

; map: rolls of paper in the warehouse
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
    
; selects array 3x3 (in most cases) around x y of arr, and counts rolls in it
(define (pick-3 arr x y)
  (let* ([size (sub1 (vector-ref (array-shape arr) 0))] ; array is square, no need to check other axle
         [clamp  ; make sure 3x3 is not going outside array area.
          (λ (a) (cond
            [(> a size) size]
            [(negative? a) 0]
            [else a]))]
         [row-from (clamp (sub1 y))] 
         [row-to (clamp (add1 y))]
         [col-from (clamp (sub1 x))]
         [col-to (clamp (add1 x))]
         [rows (in-inclusive-range row-from row-to)]
         [cols (in-inclusive-range col-from col-to)]
         [range (list rows cols)])
    (array-count positive? (array-slice-ref arr range))))  ; (rows cols)

(define (count-1 inp)
  (let* ([arr (diagram inp)]
         [size (vector-ref (array-shape arr) 0)]
         [processed-lists (for*/list ([col (in-range 0 size)]
                                      [row (in-range 0 size)])
                            (cond
                              [(zero? (array-ref arr (vector col row))) 0] ; wos nothing, keep nothing
                              [(> 5 (pick-3 arr row col)) 1] ; was less than 5 in 3x3, mark it
                              [else 0]))]) ; ignore everything else
    (for/sum ([element processed-lists]) element)))
    
(define (count-2 inp)
  (let* ([arr (diagram inp)]
         [size (vector-ref (array-shape arr) 0)])
    (let remove-rolls ([arr arr]
                       [removed 0])
      (define processed-lists
        (for*/list ([col (in-range 0 size)] ; scan all coords in array
                    [row (in-range 0 size)])
          (cond
            [(zero? (array-ref arr (vector col row))) 0] ; ignore empty areas
            [(> 5 (pick-3 arr row col)) 1] ; below 5 in 3x3, put 1 there
            [else 2]))) ; 2 - bad location
      (define result 
        ; return pair (count of removed rolls . array with new layout)
        (cons (foldl + 0 (filter odd? processed-lists))  ; sum up all 1s (good locations)
              (list->array (vector size size) ; create new array of #(size size)
                           (map (λ (element) ; with this content
                                  (cond
                                    [(zero? element) 0]
                                    [else (sub1 element)])) ; filter removed rolls (chng 2 to 1 and 1 to 0)
                                processed-lists))))
      (if (zero? (car result))
          removed ; done
          (remove-rolls (cdr result) (+ removed (car result)))))))


(display "Part 1: ")
(if (= 13 (count-1 test-input))
    (displayln (count-1 input))
    (error "wrong result"))

(time
(display "Part 2: ")
(if (= 43 (count-2 test-input))
    (displayln (count-2 input))
    (error "wrong result"))
)