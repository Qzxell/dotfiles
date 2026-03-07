set number
set showmatch
set hlsearch
set clipboard=unnamedplus
set autoindent
set splitright

syntax on

let mapleader=" "

call plug#begin()
"tabs
Plug 'nvim-tree/nvim-web-devicons' " OPTIONAL: for file icons
Plug 'romgrk/barbar.nvim'

"snippets
Plug 'SirVer/ultisnips'

Plug 'nvim-mini/mini.nvim'
Plug 'nvim-treesitter/nvim-treesitter'
Plug 'MeanderingProgrammer/render-markdown.nvim'

"telescope
Plug 'nvim-lua/plenary.nvim' " Dependencia obligatoria
Plug 'nvim-telescope/telescope.nvim'
"obsidian
Plug 'obsidian-nvim/obsidian.nvim'
Plug 'nvim-tree/nvim-web-devicons' " Iconos bonitos
Plug 'goolord/alpha-nvim'          " El motor del dashboard
call plug#end()

function! Funti()
    " 1. Obtener nombres (equivalente a BASE_NAME y ORIGINAL_NAME)
    let l:base_name = expand('%:r')
    let l:original_name = expand('%:t')
    
    if l:base_name == ""
        echo "Error: ¡No hay un archivo abierto!"
        return
    endif

    " 2. Definir rutas
    let l:new_file = l:base_name . ".md"
    let l:template_path = "/mnt/c/Users/axelt/GOICPC/Code/.temple.md"

    " 3. Verificar si el archivo ya existe
    let l:file_exists = filereadable(l:new_file)

    " 4. Abrir en split vertical
    execute 'vsplit ' . l:new_file

    " 5. Si es nuevo, inyectar plantilla y link
    if !l:file_exists
        if filereadable(l:template_path)
            " Leer plantilla desde la línea 0
            execute '0read ' . l:template_path
            
            " Ir al final del archivo e inyectar el link [[archivo.cpp]]
            call append(line('$'), ["", "[[" . l:original_name . "]]"])
            
            " Guardar para asegurar que el archivo se cree
            write
            echo "Nota '" . l:new_file . "' creada con éxito."
        else
            echo "Error: No se encontró la plantilla en " . l:template_path
        endif
    else
        echo "La nota ya existe. Abriendo..."
    endif
endfunction

" Definir el comando para usarlo como :Funti
command! Funti call Funti()

" Atajo de teclado opcional (Space + f + n)
let mapleader = " "
nnoremap <leader>fn :Funti<CR>
nnoremap <F5> :!g++ -std=c++17 -O2 -Wall -Wextra -Wshadow % -o a<CR>
nnoremap <F3> :!./a < in<CR>
nnoremap <F4> :!g++ -std=c++17 -O2 % -o a &&./a < in<CR>


tnoremap <Esc> <C-\><C-n> "exit mode insert in :term
nnoremap <C-n> :vsplit in<CR>:vertical resize 40<CR>
" Moverse al buffer anterior / siguiente con gT y gt
nnoremap <silent> gT <Cmd>BufferPrevious<CR>
nnoremap <silent> gt <Cmd>BufferNext<CR>
nnoremap <leader>e :NERDTreeToggle<CR>

nnoremap <leader>ff <cmd>Telescope find_files<cr>
nnoremap <leader>fg <cmd>Telescope live_grep<cr>
nnoremap <leader>fb <cmd>Telescope buffers<cr>

let g:UltiSnipsExpandTrigger="<tab>"
let g:UltiSnipsJumpForwardTrigger="<c-b>"

colorscheme wildcharm 

lua << EOF
require('telescope').setup{
  defaults = {
    file_ignore_patterns = { "node_modules", ".git" },
    -- Aquí puedes poner toda tu configuración en Lua
  }
}
EOF

lua << EOF
local alpha = require("alpha")
local dashboard = require("alpha.themes.dashboard")

-- 1. Tu Logo ASCII (Cualquier arte que quieras)
dashboard.section.header.val = {
    [[  > CODE OR DIE <     ]],
}

-- 2. Botones Tácticos para Programación Competitiva
dashboard.section.buttons.val = {
    dashboard.button("n", "󰈚  Nuevo Problema", ":enew <CR>"),
    dashboard.button("f", "  Buscar Archivo", ":Telescope find_files <CR>"),
    dashboard.button("c", "🧊 Ir a la Congeladora", ":Telescope live_grep default_text=congelado <CR>"),
    dashboard.button("t", "󰛢  Usar Plantilla (.temple)", ":Funti <CR>"),
    dashboard.button("q", "󰅙  Salir", ":qa<CR>"),
}

-- 3. Footer (Un toque de elegancia)
dashboard.section.footer.val = ":3"

alpha.setup(dashboard.opts)
EOF
