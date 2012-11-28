(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(case-fold-search t)
 '(column-number-mode t)
 '(display-time-mode t)
 '(global-font-lock-mode t nil (font-lock))
 '(nxhtml-default-encoding (quote utf-8))
 '(scroll-bar-mode nil)
 '(show-paren-mode t nil (paren))
 '(tab-width 4)
 '(text-mode-hook (quote (text-mode-hook-identify)))
 '(tool-bar-mode nil)
 '(uniquify-buffer-name-style (quote forward) nil (uniquify)))
(setq font-lock-maximum-decoration t)

(fset 'yes-or-no-p 'y-or-n-p) ; stop forcing me to spell out "yes"
(setq inhibit-startup-message t)
(setq inhibit-splash-screen t)
(setq backup-directory-alist '(("." . "~/.emacs-backups"))) ; stop leaving backup~ turds scattered everywhere
(add-to-list 'load-path "~/.emacs.d/site-lisp/")
(add-to-list 'load-path "~/usr/share/emacs/site-lisp/")
(add-to-list 'load-path "/usr/local/share/emacs/site-lisp/w3m/")
(add-to-list 'load-path "/usr/share/emacs/site-lisp/golang-mode/")

(setq locale-coding-system 'utf-8)
(set-terminal-coding-system 'utf-8)
(set-keyboard-coding-system 'utf-8)
(set-selection-coding-system 'utf-8)
(prefer-coding-system 'utf-8)
(set-language-environment "UTF-8")       ; prefer utf-8 for language settings


;allow a little copy and paste for more than just emacs
(setq x-select-enable-clipboard t)
(setq interprogram-paste-function 'x-cut-buffer-or-selection-value)

;;load my scratch file on load
(find-file "~/temp.txt")
(find-file "~/.emacs.d/org/d.org")


;;Interactively do
(require 'ido)
(ido-mode t)
(setq ido-enable-flex-matching t) ;; enable fuzzy matching

;; allow me to edit files on my vm with a local emacs instance
(require 'tramp)
(setq
 tramp-default-method "ssh"
 tramp-persistency-file-name "~/.emacs.d/cache/tramp")

;; recentf
(require 'recentf)    ;; save recently used files
(setq
 recentf-save-file "~/.emacs.d/cache/recentf"
 recentf-auto-cleanup 'never     ;; prevent tramp from locking up emacs
 recentf-max-saved-items 100     ;; max save 100
 recentf-max-menu-items 15)      ;; max 15 in menu
(recentf-mode t)                 ;; turn it on

(load "/usr/share/emacs/site-lisp/global/gtags.el")
(require 'gtags)
(gtags-mode t)

(add-hook 'gtags-mode-hook
  (lambda()
    (local-set-key (kbd "M-.") 'gtags-find-tag)   ; find a tag, also M-.
    (local-set-key (kbd "M-,") 'gtags-find-rtag)))  ; reverse tag

(setq ispell-program-name "aspell"
      ispell-extra-args '("--sug-mode=ultra"))

(setq-default indent-tabs-mode nil)
(setq-default tab-width 4)

;; css mode
(setq cssm-indent-level 4)
(setq cssm-newline-before-closing-bracket t)
(setq cssm-indent-function #'cssm-c-style-indenter)
(setq cssm-mirror-mode nil)

(setq auto-mode-alist
      (cons '("\\.css\\'" . css-mode) auto-mode-alist))

(load "~/.emacs.d/site-lisp/nxhtml/autostart")
;;unfortunately order matters here. nxhtml js loading is not working right now
;;it expects espresso-mode to be javascript mode as in the most recent emacs (23.3)
(autoload #'espresso-mode "espresso" "Start expresso-mode" t)
(add-to-list 'auto-mode-alist '("\\.js$" . espresso-mode))
(add-to-list 'auto-mode-alist '("\\.json$" . expreso-mode))
(setq-default indent-tabs-mode nil)
(setq-default tab-width 4)
(setq-default c-basic-offset 4)

(autoload 'geben "geben" "DBGp protocol front-end" t)

(require 'vc-svn)
(put 'scroll-left 'disabled nil)

(require 'org-install)
(add-to-list 'auto-mode-alist '("\\.org$" . org-mode))
(setq org-log-done t)

(icomplete-mode t)                      ;; completion in minibuffer
(setq
 icomplete-prospects-height 1           ;; don't spam my minibuffer
 icomplete-compute-delay 0)             ;; don't wait
(require 'icomplete+ nil 'noerror)      ;; drew adams' extras

(setq display-time-day-and-date t
      display-time-24hr-format t)
(display-time)

(require 'vc-ediff)
(eval-after-load "vc-hooks"
  '(define-key vc-prefix-map "=" 'vc-ediff))

(require 'w3m-load)
(put 'narrow-to-region 'disabled nil)

(global-auto-revert-mode 1)
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
(require 'go-mode-load)
