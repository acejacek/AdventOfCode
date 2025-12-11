#lang racket

(require 2htdp/batch-io rackunit)
(require math/matrix)

(define test-input (list
                    "123 328  51 64 "
                    " 45 64  387 23 "
                    "  6 98  215 314"
                    " *   +   *   +  "))

(define input (read-lines "Day06_input.txt"))


(define (problem-numbers inp)
  (matrix->list*  ; back to lists
   (matrix-transpose 
    (list*->matrix   ; build matrix out of lists
     (filter (negate empty?)
             (for/list ([line inp])
               (filter identity        ; filters #f from list (artefacts after regexp)
                       (if (regexp-match "[0-9]+" line)
                           (map (λ (n) (string->number n)) (regexp-split " +" line))
                           empty))))))))

(define (problem-operations inp)
  (flatten
   (filter (negate empty?)  ; ignore empty lines (with problem numbers before)
           (for/list ([line inp])
             (remove* '("") ; spaces at beg or end of line. better regexp?
                      (if (regexp-match ".*[\\*+].*" line)
                          (regexp-split " +" line) 
                          empty))))))

(define (sum-all problems operations)
  (cond
    [(empty? operations) 0] ; done
    [else
     (let* ([operand (string->symbol (car operations))]
            [problem (car problems)]
            [formula (append (list operand) problem)]) ; compose formula '(+ 1 2 49)
       ;(display formula)
       (+ (eval formula (make-base-namespace))  ; coolest trict of LISP ever
          (sum-all (cdr problems) (cdr operations))))]))
       
(define (part-1 inp)
  (let* ([problems (problem-numbers inp)]
         [operations (problem-operations inp)])
    (sum-all problems operations)))

(check-equal? (part-1 test-input) 4277556)
(display "Part 1: ")
(part-1 input)

  