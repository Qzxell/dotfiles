set number
set relativenumber
set showmatch
set hlsearch
set clipboard=unnamedplus
set autoindent
set tabstop=8               
set softtabstop=8           
set expandtab               
set shiftwidth=8

syntax on
call plug#begin()
Plug 'rebelot/kanagawa.nvim'
Plug 'sainnhe/gruvbox-material'
Plug 'morhetz/gruvbox' 
Plug 'sainnhe/sonokai'
Plug 'lifepillar/vim-solarized8'
Plug 'mhartington/oceanic-next'
Plug 'embark-theme/vim'
Plug 'sainnhe/everforest'
Plug 'itchyny/lightline.vim'
Plug 'ap/vim-css-color'
Plug 'preservim/nerdtree'
Plug 'arcticicestudio/nord-vim'
Plug 'glepnir/oceanic-material'
Plug 'rebelot/kanagawa.nvim'

Plug 'lervag/vimtex'
Plug 'SirVer/ultisnips'
call plug#end()

colorscheme OceanicNext
let g:vimtex_view_method = 'zathura'

