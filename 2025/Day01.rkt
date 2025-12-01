#lang racket

(require 2htdp/batch-io)

(define test_input '("L68" "L30" "R48" "L5" "R60" "L55" "L1" "L99" "R14" "L82"))
(define input (read-lines "Day01_input.txt"))

(define (process-list lst wheel-pos at-zero-counter)
  
  (define (inc-wheel cl)
    (modulo (+ wheel-pos cl) 100))
  (define (dec-wheel cl)
    (inc-wheel (- cl)))

  (define (at-zero? wheel-pos)
    (if (zero? wheel-pos)
        (+ at-zero-counter 1)
        at-zero-counter))

  ;(displayln wheel-pos)
   
  (if (empty? lst)
      at-zero-counter
      (if (string=? "L" (substring (car lst) 0 1))
          (process-list (cdr lst) (dec-wheel (string->number (substring (car lst) 1))) (at-zero? wheel-pos))
          (process-list (cdr lst) (inc-wheel (string->number (substring (car lst) 1))) (at-zero? wheel-pos)))))

; assert
(if (= 3 (process-list test_input 50 0))
    (process-list input 50 0)
    (error "Wrong!"))


(define (process-list-2 lst wheel-pos at-zero-counter)
  
  (define (inc-wheel cl)
    (modulo (+ wheel-pos cl) 100))
  (define (dec-wheel cl)
    (inc-wheel (- cl)))

  (define (at-zero? wheel-pos)
    (if (zero? wheel-pos)
        (+ at-zero-counter 1)
        at-zero-counter))

  (define (passing-zero? rot)
    (quotient rot 100))

  (if (empty? lst)
      at-zero-counter
      (if (string=? "L" (substring (car lst) 0 1))
          (process-list-2 (cdr lst) (dec-wheel (string->number (substring (car lst) 1))) (at-zero? wheel-pos))
          (process-list-2 (cdr lst) (inc-wheel (string->number (substring (car lst) 1))) (at-zero? wheel-pos)))))

; assert
(if (= 6 (process-list-2 test_input 50 0))
    (process-list-2 input 50 0)
    (error "Wrong!"))
