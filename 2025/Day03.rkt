#lang racket

(require 2htdp/batch-io)

(define test (list 
  "987654321111111"
  "811111111111119"
  "234234234234278"
  "818181911112111"))

(define input (read-lines "Day03_input.txt"))

(define (max-element x y) (if (> x y) x y))

;max element in list
(define (max-list ls)
    (if (null? (cdr ls))
        (car ls)
        (max-element (car ls) (max-list (cdr ls)))))

(define (index-of li element) ; rearch for index of element in list li
  (let loop ([lst li]
             [idx 0])
    (cond
      [(equal? (first lst) element) idx]
      [else (loop (rest lst) (add1 idx))])))

(define (max-joltage-1 lst)
  (for/fold ([joltage 0])
            ([bank lst])
    (let*
      ([list-of-numbers (map (λ(n) (- n 48)) (map char->integer (string->list bank)))] ; convert "123" to '(1 2 3)
       [max-element-1 (max-list list-of-numbers)]
       [max-1-idx (index-of list-of-numbers max-element-1)]
       [right-list (drop list-of-numbers (add1 max-1-idx))])
      (+ joltage
         (if (empty? right-list)
             (+ max-element-1 (* 10 (max-list (take list-of-numbers max-1-idx))))
             (+ (* 10 max-element-1) (max-list right-list)))))))
      
(if (= 357 (max-joltage-1 test))
    (max-joltage-1 input)
    (error "Wrong result"))
    