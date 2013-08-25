;; (load "rube.l")

;;;; RUBE.L
;;; Constructs the cycle decomposition of sequences of moves on the
;;; Rubik's Cube.  Faces are denoted by F, R, B, L, U and D for front,
;;; right, back, left, up and down, respectively.  Corner pieces are
;;; denoted by their three faces, or 'elements', edges by their two.
;;;
;;; Moves are denoted by their face and either: +, -, or 2, for
;;; clockwise, counterclockwise and half-turn, or no suffix, -1 and 2,
;;; for CW, CCW and half-turn.  Examples: U+, F-1, R2.
;;;
;;; Processes are given as a list of moves, e.g. '(U+ F-1 R2).  Note
;;; that the two notation styles for turns may be intermixed; however,
;;; the first style is higher in the association lists, resulting in
;;; faster lookup time.
;;;
;;; John Kerl
;;; 12/93
;;; ================================================================


;;;; -----------------------------------------------------------------------------
;; Implementation of these functions depends on the platform:

;; For CL, use "string".
;; For EL, use "prin1-to-string".
(defun symbol-to-string (sym)
  ;; (prin1-to-string sym)
  (string sym))

;; For CL, use "char".
;; For EL, use "aref".
(defun select-char-in-string (string elt)
  ;;(aref string elt)
  (char string elt))

;;;; -----------------------------------------------------------------------------
(defun cycle-decomposition (moves)
  ;; Given a list of Rubik's Cube pieces and a list of moves, return the cycle
  ;; decomposition of the moves, omitting trivial cycles.
  (delete-1-cycles (find-cycles *rube-list-of-all-pieces* moves nil)))
;; (cycle-decomposition '(F))
;; (cycle-decomposition '(F R))
;; (cycle-decomposition '(F R B L))
;; (cycle-decomposition '(F2 R2))
;; (cycle-decomposition '(F2))
;; (cycle-decomposition '(F2 B2))

(defun pprint-cycle-decomposition (moves)
  (rube-pprint (cycle-decomposition moves)))

(defun pared-moves-on-all-pieces (moves)
  (labels ((diff (image original)
		 (cond ((or (null image) (null original)) '())
		       ((equal (car image) (car original))
			(diff (cdr image) (cdr original)))
		       (t
			(cons
			 (if (rube-piece-equal (car image) (car original))
			     (cons (car original) (sign-of-rotation
						   (car original) (car image)))
			   (list (car original) '-> (car image)))
			 (diff (cdr image) (cdr original)))))))
    (diff (moves-on-pieces moves *rube-list-of-all-pieces*)
	  *rube-list-of-all-pieces*)))
;; (pared-moves-on-all-pieces '(F))
;; (setf moves '(F))


(defun moves-on-pieces (moves pieces)
  (mapcar
   #'(lambda (x)
       (moves-on-piece moves x))
   pieces))
;; (rube-piece-equal 'URF 'UFR)
;; (rube-piece-equal 'URF (moves-on-piece '(F F F F) 'UFR))

;; (moves-on-pieces '(F) '(UFR UF))
;; (moves-on-pieces '(F F) '(UFR UF))
;; (moves-on-pieces '(F F F) '(UFR UF))
;; (moves-on-pieces '(F F F F) '(UFR UF))
;; (moves-on-piece  '(F) 'UFR)
;; (moves-on-piece  '(F) 'UF)

(defun delete-1-cycles (cycles)
  (cond ((null cycles) '())
	((> (length (car cycles)) 1)
	 (cons (car cycles) (delete-1-cycles (cdr cycles))))
	(t (delete-1-cycles (cdr cycles)))))

(defun find-cycles (pieces moves current-cycles)
  (cond ((null pieces) current-cycles)
	((memtree (car pieces) current-cycles)
	 (find-cycles (cdr pieces) moves current-cycles))
	(t
	 (find-cycles
	  (cdr pieces)
	  moves
	  (append
	   current-cycles (list (find-cycle (car pieces) moves)))))))

(defun memtree (atm tree)
  ;; A predicate to determine whether non-null atom ATM is rube-equivalent
  ;; to an atomic member of TREE (i.e. if the piece given by atm is the same
  ;; piece as one in the tree, not considering spin).
  (cond ((null tree) nil)
	((not (listp tree)) (rube-piece-equal atm tree))
	;; ((equal atm tree) t) ;; would use equal outside of rube code
	;; Want to see if a piece has already been decomposed,
	;; regardless of orientation; hence the need for rube-piece-equal.
	(t (or (memtree atm (car tree))
	       (memtree atm (cdr tree))))))
;; (memtree 'F '(A B C))
;; (memtree 'F '(A F C))
;; (memtree 'F '(A (D F E) C))

(defun find-cycle (piece moves)
  (let ((cycle (list piece)))
    (do ((next (moves-on-piece moves piece)
	       (moves-on-piece moves next)))
	((rube-piece-equal piece next)
	 (append cycle (sign-of-rotation piece next)))
      (setf cycle (append cycle (list next))))))
;; (find-cycle 'UFR '(U F))

(defun sign-of-rotation (orient-1 orient-2)
  (cond ((equal orient-1 orient-2) nil) ; Same representation of same piece -- no spin.

	;; No sign if pieces aren't the same.
	((not (rube-piece-equal orient-1 orient-2)) nil)

	;; Arbitrarily, say + for any differently represented edges
	;; (rotation group only has order 2).
	((= (length (symbol-to-string orient-1)) 2) '(+))

	;; Now they must be corner pieces.  Do a table lookup.
	((member orient-1 *clockwise-orient-list*)
	 (if (char= (select-char-in-string (symbol-to-string orient-1) 1)
		    (select-char-in-string (symbol-to-string orient-2) 0))
	     '(+) '(-)))

	(t
	 (if (char= (select-char-in-string (symbol-to-string orient-1) 1)
		    (select-char-in-string (symbol-to-string orient-2) 0))
	     '(-) '(+)))))
;; (sign-of-rotation 'UFR 'UFL)
;; (sign-of-rotation 'UFR 'UFR)
;; (sign-of-rotation 'UFR 'URF)
;; (sign-of-rotation 'FUR 'FRU)
;; (sign-of-rotation 'UFR 'UR)

;; The names of three adjacent faces provide the name of a corner piece;
;; the names of two adjacent faces provide the name of an edge piece.
;; However, a corner's three faces may be combined in any of six (3!) ways, e.g.
;; URF, UFR, FRU, FUR, RFU, and RUF; and an edge's two faces may be combined
;; in one of two (2!) ways, e.g. UF and FU.
;;
;; This function sees if two representations refer to the same piece.
;; E.g. UFR is the same as FRU; UFR is not the same as UFL; UFR is not the
;; same as UF.

(defun rube-piece-equal (piece-1 piece-2)
  (let ((length-1 (length (symbol-to-string piece-1)))
	(length-2 (length (symbol-to-string piece-2))))
    (cond ((not (= length-1 length-2))
	   nil);; Edges and corners can't possibly be the same!

	  ((= length-1 3)		; Corner piece; there are 6 permutations of elts to consider.
	   (let* ((p1 (symbol-to-string piece-1))
		  (p2 (symbol-to-string piece-2))
		  (p11 (select-char-in-string p1 0))
		  (p12 (select-char-in-string p1 1))
		  (p13 (select-char-in-string p1 2))
		  (p21 (select-char-in-string p2 0))
		  (p22 (select-char-in-string p2 1))
		  (p23 (select-char-in-string p2 2)))
	     (or
	      (and (char= p11 p21) (char= p12 p22) (char= p13 p23))
	      (and (char= p11 p21) (char= p12 p23) (char= p13 p22))
	      (and (char= p11 p22) (char= p12 p21) (char= p13 p23))
	      (and (char= p11 p22) (char= p12 p23) (char= p13 p21))
	      (and (char= p11 p23) (char= p12 p21) (char= p13 p22))
	      (and (char= p11 p23) (char= p12 p22) (char= p13 p21)))))

	  ((= length-1 2)		; Edge piece; there are 2 permutation of elts to consider.
	   (let* ((p1 (symbol-to-string piece-1))
		  (p2 (symbol-to-string piece-2))
		  (p11 (select-char-in-string p1 0)) (p12 (select-char-in-string p1 1))
		  (p21 (select-char-in-string p2 0)) (p22 (select-char-in-string p2 1)))
	     (or
	      (and (char= p11 p21) (char= p12 p22))
	      (and (char= p12 p21) (char= p11 p22)))))

	  ;; The 't' statement keeps this predicate from returning #<unspecified> in Scheme.
	  (t (equal piece-1 piece-2)))))
;; (rube-piece-equal 'UFR 'URF)
;; (rube-piece-equal 'UFR 'URL)
;; (rube-piece-equal 'UFR 'UF)

(defun moves-on-piece (moves piece)
  ;; Need to tune this (auxiliary function?) so that it
  ;; doesn't check the same piece over and over for corner/edge.
  ;; Once passed in, it won't change!
  (cond ((= 3 (length (symbol-to-string piece)))
	 (if (null moves)
	     piece
	   (moves-on-piece
	    (cdr moves)
	    (move-on-corner-piece (car moves) piece))))
	((= 2 (length (symbol-to-string piece)))
	 (if (null moves)
	     piece
	   (moves-on-piece
	    (cdr moves)
	    (move-on-edge-piece (car moves) piece))))))
;; (moves-on-piece '(U F R) 'UFR)


;; Returns the image of a corner piece under a move.
;; Breaks the piece up into its component faces; looks up the image
;; of each face under the specifed move; then puts the resulting
;; faces back together.
;;
;; What the if-statement does is, if the move (denoted by a face)
;; isn't on the same face as one of the piece's faces, then the
;; piece is unaffected by the move.  E.g. URF is affected by F;
;; but URL is not.
;;
;; Both arguments are represented by symbols.
(defun move-on-corner-piece (move corner)
  (let* ((ps (symbol-to-string corner))
	 (ps0 (select-char-in-string ps 0))
	 (ps1 (select-char-in-string ps 1))
	 (ps2 (select-char-in-string ps 2))
	 (face (select-char-in-string (symbol-to-string move) 0)))
    (if (or (equal face ps0) (equal face ps1) (equal face ps2))
	(intern
	 (concatenate 'string
		      (symbol-to-string (move-on-face move ps0))
		      (symbol-to-string (move-on-face move ps1))
		      (symbol-to-string (move-on-face move ps2))))
					; else
      corner)))
;; (move-on-corner-piece 'F 'URF)
;; (move-on-corner-piece 'F 'URL)

;; Returns the image of an edge piece under a move.
;; Breaks the piece up into its component faces; looks up the image
;; of each face under the specifed move; then puts the resulting
;; faces back together by turning a string into a symbol.
;; (See Steele's CLTL for a description of the difference between
;; intern and make-symbol.  For me, the relevant difference is that
;; a symbol created with make-symbol prints with a leading #: (ugly),
;; whereas a symbol created with intern doesn't (pretty).
;;
;; What the if-statement does is, if the move (denoted by a face)
;; isn't on the same face as one of the piece's faces, then the
;; piece is unaffected by the move.  E.g. UF is affected by F;
;; but UR is not.
;;
;; Both arguments are represented by symbols.
(defun move-on-edge-piece (move edge)
  (let* ((ps (symbol-to-string edge))
	 (ps0 (select-char-in-string ps 0))
	 (ps1 (select-char-in-string ps 1))
	 (face (select-char-in-string (symbol-to-string move) 0)))
    (if (or (equal face ps0)
	    (equal face ps1))
	(intern
	 ;;string->symbol
	 (concatenate 'string
		      (symbol-to-string (move-on-face move ps0))
		      (symbol-to-string (move-on-face move ps1))))
      ;; else
      edge)))

;; (move-on-edge-piece 'F 'UF)
;; (move-on-edge-piece 'F 'UR)
;; (setf edge 'UF)
;; (setf move 'F)
;; (setf ps (symbol-to-string edge))
;; (setf ps0 (select-char-in-string ps 0))
;; (setf ps1 (select-char-in-string ps 1))
;; (setf face (select-char-in-string (symbol-to-string move) 0))

;; (string->symbol "abc")
;; (apropos 'symbol)
;; (symbol "abc")


;; Returns the image of a face under a move.
;; Faces are represented by characters; moves are represented by symbols.
;; Does a simple table lookup.
(defun move-on-face (move face)
  (let ((row-vector   (assoc face *move-on-face-table*))
	(vector-index (assoc move *move-index-lookup-alist*)))
    (cond ((equal nil row-vector)
	   (error
	    (format nil
		    "move-on-face:  Rule lookup failed for face ~A.~%"
		    (cond ((symbolp face) (symbol-to-string face))
			  ((stringp face) face)
			  ((characterp face) (symbol-to-string face))))))
	  ((equal nil vector-index)
	   (error
	    (format nil
		    "move-on-face:  Rule lookup failed for move ~A.~%"
		    (cond ((symbolp move) (string move))
			  ((stringp move) move)
			  ((characterp move) (symbol-to-string move))))))
	  (t (aref (cdr row-vector) (cdr vector-index))))))
;; (move-on-face 'U #\F)
;; (setf face #\F)
;; (setf move 'U)


;;;; -----------------------------------------------------------------------------
;;;; RUBE DATA SECTION -- lookup tables.

;; The names of three adjacent faces provides the name of a corner piece.
;; However, those three faces may be combined in any of six ways, e.g.
;; URF, UFR, FRU, FUR, RFU, and RUF.
;; This variable contains all such names in which the faces are listed
;; in a clockwise direction.  This could be calculated at run-time,
;; but it seems simpler to do a table lookup.
(defvar *clockwise-orient-list*
  '(URF UFL ULB UBR DFR DRB DBL DLF
	RFU FLU LBU BRU FRD RBD BLD LFD
	FUR LUF BUL RUB RDF BDR LDB FDL))

;; Data for the image of a face under a move.  Faces are down the table; moves are across.
;; Faces are represented as characters; moves are represented by symbols.
;; Key into this table by face to get an array of images of that face.
;; Index into the resulting array, using the *move-index-lookup-alist*, to get
;; the image of the specified face under the specified move.
(defvar *move-on-face-table*

  ;;  F+  R+  B+  L+  U+  D+  F-  R-  B-  L-  U-  D-  F2  R2  B2  L2  U2  D2
  ;; FRBLUD going down
  '((#\F . #( #\F #\U #\F #\D #\L #\R #\F #\D #\F #\U #\R #\L #\F #\B #\F #\B #\B #\B ))
    (#\R . #( #\D #\R #\U #\R #\F #\B #\U #\R #\D #\R #\B #\F #\L #\R #\L #\R #\L #\L ))
    (#\B . #( #\B #\D #\B #\U #\R #\L #\B #\U #\B #\D #\L #\R #\B #\F #\B #\F #\F #\F ))
    (#\L . #( #\U #\L #\D #\L #\B #\F #\D #\L #\U #\L #\F #\B #\R #\L #\R #\L #\R #\R ))
    (#\U . #( #\R #\B #\L #\F #\U #\U #\L #\F #\R #\B #\U #\U #\D #\D #\D #\D #\U #\R ))
    (#\D . #( #\L #\F #\R #\B #\D #\D #\R #\B #\L #\F #\D #\D #\U #\U #\U #\U #\D #\D ))))

;; See above comment.
(defvar *move-index-lookup-alist*
  '((F+  .  0) (R+  .  1) (B+  .   2) (L+  .  3) (U+  .  4) (D+  .  5)
    (F-  .  6) (R-  .  7) (B-  .   8) (L-  .  9) (U-  . 10) (D-  . 11)
    (F2  . 12) (R2  . 13) (B2  .  14) (L2  . 15) (U2  . 16) (D2  . 17)
    (F   .  0) (R   .  1) (B   .   2) (L   .  3) (U   .  4) (D   .  5)
    (F-1 .  6) (R-1 .  7) (B-1 .   8) (L-1 .  9) (U-1 . 10) (D-1 . 11)
    (f+  .  0) (r+  .  1) (b+  .   2) (l+  .  3) (u+  .  4) (d+  .  5)
    (f-  .  6) (r-  .  7) (b-  .   8) (l-  .  9) (u-  . 10) (d-  . 11)
    (f2  . 12) (r2  . 13) (b2  .  14) (l2  . 15) (u2  . 16) (d2  . 17)
    (f   .  0) (r   .  1) (b   .   2) (l   .  3) (u   .  4) (d   .  5)
    (f-1 .  6) (r-1 .  7) (b-1 .   8) (l-1 .  9) (u-1 . 10) (d-1 . 11)))

;; A table to show the inverse of any move.
(defvar *invert-move-alist*
  '((F+ . F-) (R+ . R-) (B+ . B-) (L+ . L-) (U+ . U-) (D+ . D-)
    (F- . F+) (R- . R+) (B- . B+) (L- . L+) (U- . U+) (D- . D+)
    (F2 . F2) (R2 . R2) (B2 . B2) (L2 . L2) (U2 . U2) (D2 . D2)
    (F  . F-) (R  . R-) (B  . B-) (L  . L-) (U  . U-) (D  . D-)
    (F- . F ) (R- . R ) (B- . B ) (L- . L ) (U- . U ) (D- . D )
    (f+ . f-) (r+ . r-) (b+ . b-) (l+ . l-) (u+ . u-) (d+ . d-)
    (f- . f+) (r- . r+) (b- . b+) (l- . l+) (u- . u+) (d- . d+)
    (f2 . f2) (r2 . r2) (b2 . b2) (l2 . l2) (u2 . u2) (d2 . d2)
    (f  . f-) (r  . r-) (b  . b-) (l  . l-) (u  . u-) (d  . d-)
    (f- . f ) (r- . r ) (b- . b ) (l- . l ) (u- . u ) (d- . d )))

;; A table of all the movable pieces (i.e., not including centers)
;; on the cube.
(defvar *rube-list-of-all-pieces*
  '(UFR UFL UBL UBR DFR DFL DBL DBR
	UF UL UB UR FR FL BL BR DF DL DB DR))

;;;; -----------------------------------------------------------------------------
;;;; RUBE EXPONENT SECTION

;; Inverting a list of moves means reversing it and replacing each
;; individual move with its inverse -- ( A * B )^-1 = B^-1 * A^-1.
(defun invert-moves (proc)
  (cond ((null proc) '())
	((not (listp proc)) (list proc))
	(t
	 (append (invert-moves (cdr proc))
		 (list (invert-move (car proc)))))))
(defun invert-move (move)
  (let ((inv (assoc move *invert-move-alist*)))
    (cond ((equal nil inv)
	   (error
	    (string-append
	     "invert-move:  Couldn\'t find inverse for "
	     (cond ((symbolp move) (symbol-to-string move))
		   ((characterp   move) (symbol-to-string move)))
	     "\n")))
	  (t (cdr inv)))))
(defun power-of-sequence (moves power)
  (cond ((= power 0) '())
	((= power 1) moves)
	((> power 1)
	 (append moves (power-of-sequence moves (- power 1))))
	((= power -1) (invert-moves moves))
	((< power -1) (power-of-sequence
		       (invert-moves moves)
		       (- power)))))
(defun rube-conjugate (proc1 proc2)
  ;; This returns the conjugate of A by B, denoted A * B * A^-1.
  (let ((lproc1 (if (symbolp proc1) (list proc1) proc1))
	(lproc2 (if (symbolp proc2) (list proc2) proc2)))
    (append lproc1 lproc2 (invert-moves lproc1))))

;; This returns the commutator of two moves or list of moves on the
;; Rubik's Cube.  In group theory, the commutator of A and B, denoted
;; by [A B], is defined to be A * B * A^-1 * B^-1.  [A B] == the identity
;; sequence precisely when A and B commute (i.e. when A*B == B*A).
(defun commutator (proc1 proc2)
  (let ((lproc1 (if (symbolp proc1) (list proc1) proc1))
	(lproc2 (if (symbolp proc2) (list proc2) proc2)))
    (append lproc1 lproc2
	    (invert-moves lproc1) (invert-moves lproc2))))
;; (defun order (cycle-list)
;; 		(apply #'lcm (map cycle-length cycle-list)))
(defun order (moves)
  (apply #'lcm (mapcar #'cycle-length (cycle-decomposition moves))))
(defun cycle-length (cycle)
  (cond ((or (equal (last cycle) '+)
	     (equal (last cycle) '-))
	 (let ((edge-or-corner
		(length (symbol-to-string (car cycle)))))
	   (cond ((= edge-or-corner 3)
		  (* 3 (- (length cycle) 1)))
		 ((= edge-or-corner 2)
		  (* 2 (- (length cycle) 1)))
		 (t (length cycle)))))
	(t (length cycle))))

;;;; -----------------------------------------------------------------------------
;;;; RUBE PPRINT SECTION

;; This is a function to print output of cycle-decompose with nice line breaks.
;; Actually what is does is print the elements of any list one line at a time.
(defun rube-pprint (lst)
  (labels
      ((rube-pprint-aux (lst)
			(cond
			 ((null lst) nil)
			 ((not (consp lst)) (format t "~A~%" lst))
			 (t
			  (progn
			    (format t "~A~%" (car lst))
			    (rube-pprint-aux (cdr lst)))))))
    (rube-pprint-aux lst))
  (values))
;; (rube-pprint '(a b c d e))
;; (rube-pprint '((a b) (c d) (e f)))

;;;; -----------------------------------------------------------------------------
;;;; TESTS

;; (mapcar #'(lambda (x)	  (move-on-face 'U x)) '(#\F #\R #\B #\L #\U #\D))

;; (setf forward-moves  '(F R B L U D))
;; (setf backward-moves '(F- R- B- L- U- D-))
;; (setf double-moves   '(F2 R2 B2 L2 U2 D2))

;; (mapcar #'(lambda (x) (move-on-edge-piece x 'UF)) forward-moves)
;; (mapcar #'(lambda (x) (move-on-edge-piece x 'UF)) backward-moves)
;; (mapcar #'(lambda (x) (move-on-edge-piece x 'UF)) double-moves)

;; (mapcar #'(lambda (x) (move-on-edge-piece x 'FU)) forward-moves)
;; (mapcar #'(lambda (x) (move-on-edge-piece x 'FU)) backward-moves)
;; (mapcar #'(lambda (x) (move-on-edge-piece x 'FU)) double-moves)

;; (mapcar #'(lambda (x) (move-on-corner-piece x 'UFR)) forward-moves)
;; (mapcar #'(lambda (x) (move-on-corner-piece x 'UFR)) backward-moves)
;; (mapcar #'(lambda (x) (move-on-corner-piece x 'UFR)) double-moves)

;; (rube-piece-equal 'UFR 'FRU)
;; (rube-piece-equal 'Ufr 'FUR)
;; (rube-piece-equal 'FUR 'FUR)
;; (rube-piece-equal 'FUR 'FU)
;;
;; (sign-of-rotation 'UFR 'FRU)
;; (sign-of-rotation 'UFR 'UFR)
;; (sign-of-rotation 'UFR 'URF)
;; (sign-of-rotation 'UFR 'FR)
;; (sign-of-rotation 'RF 'FR)
;; (sign-of-rotation 'RF 'RF)
;;
;; (memtree 'UF '(FR UR BL DL))
;; (memtree 'U '(F R B U))
;; (rube-piece-equal 'U 'F)
;; (moves-on-piece '(F) (moves-on-piece '(F) (moves-on-piece '(F)(moves-on-piece '(F) 'UFR))))
;;
;; (find-cycle 'UFR '(F))
;; (find-cycle 'UF '(U2))
;; (find-cycle 'UFR '(F))
;; (find-cycle 'UFR '(F R B L))
;; (find-cycle 'UF '(B))
;; (find-cycle 'UF '(F R))
;; (find-cycle 'UF (power-of-sequence '(F2 R2) 2))
;; (find-cycle 'UF (power-of-sequence '(F2 R2) 3))
;; (find-cycle 'UFR '(F R))
;; (find-cycle 'UFR '(F R B L))
;;
;; (invert-moves '(F+ R+ B+ L+))
;; (rube-conjugate '(F R) '(B L))
;; (commutator '(F R) '(B L))
;; (rube-conjugate '(B) (power-of-sequence '(L U L- U-) 3))
;;
;; (cycle-decomposition '(F R B L))
;; (cycle-decomposition (power-of-sequence '(F R) 2))
;; (cycle-decomposition '(B- U2 B2 U B- U- B- U2 F R B R- F-))
;; (cycle-decomposition '(R L- F R- L D2 R L- F R- L))
;; (cycle-decomposition (power-of-sequence '(B R- D2 R B- U2) 1))
;; (cycle-decomposition (power-of-sequence '(B R- D2 R B- U2) 2))
;; (cycle-decomposition (power-of-sequence '(F R) 2))
;; (cycle-decomposition (power-of-sequence '(F2 R2) 6))
;; (cycle-decomposition
;;   '(R L- F  R- L D
;;  	 R L- F  R- L D
;;  	 R L- F2 R- L D
;;  	 R L- F  R- L D
;;  	 R L- F  R- L D2))
;; (moves-on-pieces (power-of-sequence '(B R- D2 R B- U2) 2) *rube-list-of-all-pieces*)
;; (moves-on-pieces '(R L- F R- L D2 R L- F R- L) '(DR DB DL))
;; (moves-on-pieces '(R L- F R- L D2 R L- F R- L) *rube-list-of-all-pieces*)
;; (moves-on-pieces (power-of-sequence '(B R- D2 R B- U2) 2) *rube-list-of-all-pieces*)
;; (pared-moves-on-all-pieces '(R L- F R- L D2 R L- F R- L))
;; (pared-moves-on-all-pieces (power-of-sequence '(B R- D2 R B- U2) 2))
;; (pared-moves-on-all-pieces (power-of-sequence '(F2 R2) 2))
;;
;; (order (power-of-sequence '(B R- D2 R B- U2) 2))
;; (order '(R L- F R- L D2 R L- F R- L))
;; (order '(R L- F R- L D2 R L- F R- L))
;; (order (power-of-sequence '(B R- D2 R B- U2) 2))
;; (order '(R L- F R- L D2 R L- F R- L))
;; (order (power-of-sequence '(B R- D2 R B- U2) 2))
;; (order (power-of-sequence '(F2 R2) 2))
;; (order '(F R B L))
;; (order '(F2 R2))
;; (order '(F R))
;; (order '(F R-))
;; (order '(F R2))
;; (order '(F U R))
;; (order '(F U R B D L))
;; (order '(F U R B L D))
;; (order '(F))
;;

;; (setf moves '(F2 R2))

(defun tell-about (moves)
  (format t "-- Sequence is: ~%~A~%~%" moves)
  (format t "-- Image is: ~%~A~%~%" (pared-moves-on-all-pieces moves))
  (format t "-- Cycle decomposition is: ~%~A~%~%" (cycle-decomposition moves))
  (format t "-- Order is: ~%~A~%~%" (order moves))
  (values))

(defun tell-about (moves)
  (format t "~%-- Sequence is: ~%~A~%" moves)
  (format t "~%-- Image is: ~%")
  (rube-pprint (pared-moves-on-all-pieces moves))
  (format t "~%-- Cycle decomposition is: ~%")
  (rube-pprint (cycle-decomposition moves))
  (format t "~%-- Order is: ~%~A~%~%" (order moves))
  (values))

;; (values) to avoid having a return value from this defun print out.

;; rube-pprint prints each element of a list on a line by itself;
;; format with a ~A prints all the elements of a list on one line.
;;
;; So I could use these in tell-about -- having each list element on a
;; single line makes output more readable, but on the other hand makes
;; the window scroll a lot.  Kind of a trade-off.  For now, I'm not
;; using these.

;;	 (rube-pprint (pared-moves-on-all-pieces moves))
;;	 (rube-pprint (cycle-decomposition moves))


;; (tell-about '(F))
;; (tell-about (power-of-sequence '(B R- D2 R B- U2) 2))
;; (tell-about '(R L- F R- L D2 R L- F R- L))
;; (tell-about (power-of-sequence '(F2 R2) 2))
;; (tell-about '(F R B L))
;; (tell-about '(F R B L D U))
;; (tell-about '(R L- F  R- L D
;; 	 R L- F  R- L D
;; 	 R L- F2 R- L D
;; 	 R L- F  R- L D
;; 	 R L- F  R- L D2))
