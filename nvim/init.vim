set nocompatible            " disable compatibility to old-time vi
set showmatch               " show matching 
set ignorecase              " case insensitive 
set mouse=v                 " middle-click paste with 
set hlsearch                " highlight search 
set incsearch               " incremental search
set tabstop=4               " number of columns occupied by a tab 
set softtabstop=4           " see multiple spaces as tabstops so <BS> does the right thing
set expandtab               " converts tabs to white space
set shiftwidth=4            " width for autoindents
set autoindent              " indent a new line the same amount as the line just typed
set relativenumber                  " add line numbers
set number                  " add line numbers
set wildmode=longest,list   " get bash-like tab completions
" set cc=80                   " set an 80 column border for good coding style
filetype plugin indent on   "allow auto-indenting depending on file type
syntax on                   " syntax highlighting
set mouse=a                 " enable mouse click
set clipboard=unnamedplus   " using system clipboard
filetype plugin on
" set cursorline              " highlight current cursorline
set ttyfast                 " Speed up scrolling in Vim
call plug#begin()
Plug 'junegunn/vim-easy-align'
Plug 'farmergreg/vim-lastplace'

Plug 'https://github.com/junegunn/vim-github-dashboard.git'
Plug 'preservim/nerdtree', { 'on': 'NERDTreeToggle' }
Plug 'tpope/vim-fireplace', { 'for': 'clojure' }

Plug 'rdnetto/YCM-Generator', { 'branch': 'stable' }

Plug 'fatih/vim-go', { 'tag': '*' }

Plug 'nsf/gocode', { 'tag': 'v.20150303', 'rtp': 'vim' }

Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }

Plug '~/my-prototype-plugin'
Plug 'rebelot/kanagawa.nvim'
Plug 'sainnhe/gruvbox-material'
Plug 'ajmwagar/vim-deus'
Plug 'sheerun/vim-polyglot'
Plug 'morhetz/gruvbox' 
Plug 'sainnhe/sonokai'
Plug 'preservim/nerdcommenter'
Plug 'ap/vim-buftabline'
Plug 'lifepillar/vim-solarized8'
Plug 'mhartington/oceanic-next'
Plug 'embark-theme/vim'
Plug 'sainnhe/everforest'
Plug 'itchyny/lightline.vim'
Plug 'airblade/vim-gitgutter'
Plug 'ap/vim-css-color'
Plug 'preservim/nerdtree'
Plug 'arcticicestudio/nord-vim'
Plug 'glepnir/oceanic-material'
Plug 'rebelot/kanagawa.nvim'

Plug 'lervag/vimtex'
Plug 'SirVer/ultisnips'
call plug#end()

command! -nargs=0 CopileRunShow :w | execute '!g++ -o a ' . expand('%') . '&& ./a < in > ou' | vs ou
command! -nargs=0 CopileRun :w | execute '!g++ -o a ' . expand('%') . '&& ./a < in ' 
command! -nargs=0 CopileRunCF :w | execute '!g++ -o a ' . expand('%') . '&& /home/qzxl/scripts/cff a ' .expand('%:t:r')  | vs ou


let mapleader=" "
set hidden
nnoremap <silent> <S-l> :bnext<CR>
nnoremap <silent> <S-h> :bprev<CR>
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l
nnoremap <Leader>vs :vs<CR>  
nnoremap <Leader>vp :sp <CR> 
nnoremap <Leader>cp ggVGy <CR> 
nnoremap <Leader>rm  ggVGd <CR> 
nnoremap <Leader>e  :NERDTreeToggle <CR> 

map <F5> :CopileRunShow <CR>
map <F4> :CopileRun <CR>
map <F2> :CopileRunCF <CR>
map <F3> :!./a < in <CR>



let g:vimtex_view_method = 'zathura'

autocmd! BufReadPost *
    \ if line("'\"") > 1 && line("'\"") <= line("$") | 
    \   exe "normal! g´\"" |
    \endif


colorscheme kanagawa

