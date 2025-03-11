(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(ansi-color-faces-vector
   [default default default italic underline success warning error])
 '(ansi-color-names-vector
   ["#242424" "#e5786d" "#95e454" "#cae682" "#8ac6f2" "#333366" "#ccaa8f" "#f6f3e8"])
 '(case-fold-search t)
 '(column-number-mode t)
 '(css-indent-offset 2)
 '(custom-enabled-themes (quote (tsdh-dark)))
 '(custom-safe-themes
   (quote
    ("bc89fda3d232a3daa4eb3a9f87d6ffe1272fea46e4cf86686d9e8078e4209e2c" default)))
 '(display-time-mode t)
 '(flycheck-php-phpcs-executable nil)
 '(fringe-mode 6 nil (fringe))
 '(global-font-lock-mode t nil (font-lock))
 '(js-indent-level 2)
 '(linum-format (quote dynamic))
 '(org-agenda-files (quote ("~/.emacs.d/org/d.org")))
 '(package-selected-packages
   (quote
    (hcl-mode htmlize quickrun tramp projectile helm flycheck exec-path-from-shell web-mode kotlin-mode groovy-mode nginx-mode markdown-mode terraform-mode docker-compose-mode dockerfile-mode js2-mode vue-mode ag find-file-in-repository magit php-mode yaml-mode)))
 '(save-place t)
 '(scroll-bar-mode nil)
 '(show-paren-mode t nil (paren))
 '(standard-indent 2)
 '(text-mode-hook (quote (text-mode-hook-identify)))
 '(tool-bar-mode nil)
 '(uniquify-buffer-name-style (quote forward) nil (uniquify)))
(setq font-lock-maximum-decoration t)

(require 'package)
(add-to-list 'package-archives '("melpa" . "http://melpa.milkbox.net/packages/") t)
(add-to-list 'package-archives '("marmalade" . "http://marmalade-repo.org/packages/"))
(package-initialize)

(fset 'yes-or-no-p 'y-or-n-p) ; stop forcing me to spell out "yes"
(setq inhibit-startup-message t)
(setq inhibit-splash-screen t)
(setq backup-directory-alist '(("." . "~/.emacs-backups"))) ; stop leaving backup~ turds scattered everywhere

(setq locale-coding-system 'utf-8)
(set-terminal-coding-system 'utf-8)
(set-keyboard-coding-system 'utf-8)
(set-selection-coding-system 'utf-8)
(prefer-coding-system 'utf-8)
(set-language-environment "UTF-8")       ; prefer utf-8 for language settings

;allow a little copy and paste for more than just emacs
(setq x-select-enable-clipboard t)
;(setq interprogram-paste-function 'x-cut-buffer-or-selection-value)

;;load my scratch file on load
(find-file "~/temp.txt")
(find-file "~/.emacs.d/org/d.org")
(find-file "~/Projects/spark_secure_causes-amzn2_dev_local/data/web/dev/wpg.develop")


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

(setq ispell-program-name "aspell"
      ispell-extra-args '("--sug-mode=ultra"))

(setq-default indent-tabs-mode nil)

;(autoload 'geben "geben" "DBGp protocol front-end" t)


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

;;ln -s ~/Projects/git/contrib/emacs/ ./git
(add-to-list 'load-path "~/.emacs.d/lisp/")
(add-to-list 'load-path "~/Source/git/contrib/emacs/")
(require 'hcl-mode)
(add-to-list 'auto-mode-alist '("\\.tf\\'" . hcl-mode))
;(require 'vc-ediff)
;(require 'git)
;(require 'git-blame)
(eval-after-load "vc-hooks"
  '(define-key vc-prefix-map "=" 'vc-ediff))

;; (require 'w3m-load)

(global-auto-revert-mode 1)
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(default ((t (:inherit nil :stipple nil :background "gray20" :foreground "white smoke" :inverse-video nil :box nil :strike-through nil :overline nil :underline nil :slant normal :weight normal :height 110 :width normal :foundry "nil" :family "Monaco")))))

(put 'narrow-to-region 'disabled nil)

(add-to-list 'auto-mode-alist '("\\.phtml\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.tpl\\.php\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.html\\.twig\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.html?\\'" . web-mode))

(setq web-mode-engines-alist
      '(("php"    . "\\.phtml\\'")
        ("blade"  . "\\.blade\\."))
)

(defun my-web-mode-hook ()
  "Hooks for Web mode."
  (setq web-mode-markup-indent-offset 2)
  (setq web-mode-code-indent-offset 2)
)
(add-hook 'web-mode-hook  'my-web-mode-hook)


(setq web-mode-enable-current-element-highlight t)
(put 'narrow-to-page 'disabled nil)

;enables spell check on OSX
(add-to-list 'exec-path "/usr/local/bin")
(setq ispell-programm-name "aspell")

;js2-mode
(add-to-list 'auto-mode-alist '("\\.js\\'" . js2-mode))

(global-set-key (kbd "C-x f") 'find-file-in-repository)

;enables ag
(setenv "PATH" (concat (getenv "PATH") ":/usr/local/bin"))

;; setup file ending in ".module" to open in php-mode
(add-to-list 'auto-mode-alist '("\\.module\\'" . php-mode))
;; setup file ending in ".inc" to open in php-mode
(add-to-list 'auto-mode-alist '("\\.inc\\'" . php-mode))
;; setup file ending in ".inc" to open in php-mode
(add-to-list 'auto-mode-alist '("\\.install\\'" . php-mode))

;; Sets tab width to 2 spaces in php mode.
;; (add-hook 'php-mode-hook 'my-php-mode-hook)
;; (defun my-php-mode-hook ()
;;   "My PHP mode configuration."
;;   (setq indent-tabs-mode nil
;;         tab-width 2
;;         c-basic-offset 2))

(defun my-php-mode-hook ()
  "My PHP mode configuration."
  (setq tab-width 2
        c-basic-offset 2))
;(put 'downcase-region 'disabled nil)

;;(add-hook 'terraform-mode-hook #'terraform-format-on-save-mode)


(require 'quickrun)

(when (memq window-system '(mac ns x))
  (exec-path-from-shell-initialize))
(add-hook 'after-init-hook #'global-flycheck-mode)

(require 'projectile)
(projectile-mode +1)

(setq projectile-project-search-path '("~/projects/"))
(require 'helm)

(add-hook 'php-mode-hook #'(lambda()
                             (php-enable-drupal-coding-style)
                             (setq c-basic-offset 2)))
;; (add-to-list 'load-path "/Users/deifantewalters/Projects/Personal/emacs-htmlize/htmlize.el")
(add-to-list 'load-path "/Users/deifantewalters/Projects/Personal/emacs-htmlize/")
(require 'htmlize)

