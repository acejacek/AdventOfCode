#lang racket

(require 2htdp/batch-io rackunit)
(require math/matrix)

(define test-input (list
                    "123 328  51 64 "
                    " 45 64  387 23 "
                    "  6 98  215 314"
                    " *   +   *   + "))



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

; input -> list of bytes, index, and offset = length of line
; result (432 12 34 56 2) array of vertically decoded numbers, and in last column index of next group
(define  (proc-group merged offset i)
    
  (let ([column-sum (for/fold ([result 0])
                              ([ver (in-range i (bytes-length merged) offset)]) ; walk all verses in input
                      ; convert bytes to digits, ignore everything what os not digit
                      (let* ([nbr (- (bytes-ref merged ver) 48)]
                             [nbr (if (negative? nbr)
                                      0
                                      nbr)])
                        (cond
                          [(zero? nbr) result] ; there was no single digit in column, it's end of group then
                          [else (+ (* 10 result) nbr)])))]) ; process next column
    (cond
      ; of sum is 0, then all digits in cilumn sum to zero, means end of group
      [(zero? column-sum) (cons (add1 i) empty)] ; done. attach index of column next calc should start from
      [(>= i offset) (cons i empty)] ; very last element od byte string
      [else
       (cons column-sum (proc-group merged offset (add1 i)))])))

; this generates same looking list of problems as (problem-operations) from part 1
; just need to build it vertically
(define (process-all inp)
  (let* ([ls (for/list ([line inp])          ; read input as strings
               (string->bytes/locale line))] ; convert to byte-strings
         [long-bytes (bytes-append* ls)] ; merge into one long pass
         [len (bytes-length (car ls))]) ; but keep length of individual line, will be needed as offset
    (let scan ([i 0])            ; start scanning from column 0
      (let* ([result (proc-group long-bytes len i)]
             [group-number (drop-right result 1)]
             [new-idx (last result)])
        (cond
          [(> len new-idx) (cons group-number (scan new-idx))]
          [else (cons group-number empty)])))))

(define (part-2 inp)
  (let* ([problems (process-all inp)]
         [operations (problem-operations inp)])
    (sum-all problems operations)))

(check-equal? (part-2 test-input) 3263827)
(display "Part 2: ")
(part-2 input)










