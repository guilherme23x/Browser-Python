import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLineEdit, QPushButton, QToolBar
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt

class BrowserTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Cria um WebView
        self.browser = QWebEngineView()
        self.layout.addWidget(self.browser)

        # Carregar a homepage padrão
        self.browser.setUrl(QUrl("http://www.google.com"))  # Definindo a homepage padrão

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        self.browser.setUrl(QUrl(url))

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navegador com Abas")
        self.setGeometry(100, 100, 1200, 800)

        # Define o estilo da janela
        self.setStyleSheet("background-color: #202222;")  # Fundo da janela

        # Cria um TabWidget e define a cor da borda
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 0px solid #20B8CD; }  /* Cor da borda das abas */
            QTabBar::tab { background: #202222; color: white; padding: 10px; placeholder: "Digite uma URL aqui";}
            QTabBar::tab:selected { background: #20B8CD; color: black; }  /* Cor da aba selecionada */
            QTabBar::tab:hover { background: #333; color: white; }  /* Cor da aba ao passar o mouse */
        """)
        self.setCentralWidget(self.tabs)

        # Adiciona a primeira aba
        self.add_new_tab()

        # Barra de pesquisa
        self.search_bar = QLineEdit()
        self.search_bar.setStyleSheet("border: 2px solid #20B8CD; color: white; padding: 10px;margin: 2px; border-radius: 10px; font-size: 16px")
        self.search_bar.returnPressed.connect(self.navigate_to_url)

        # Toolbar para botões de navegação
        self.toolbar = QToolBar("Navegação")
        self.toolbar.addWidget(self.search_bar)
        self.addToolBar(self.toolbar)

        # Estilo dos botões
        button_style = "background-color: #20B8CD; color: black; border: none; padding: 10px; margin: 1px; border-radius: 10px;"

        # Botão "Voltar"
        self.back_button = QPushButton("Voltar")
        self.back_button.setStyleSheet(button_style)
        self.back_button.clicked.connect(self.go_back)
        self.toolbar.addWidget(self.back_button)

        # Botão "Avançar"
        self.forward_button = QPushButton("Avançar")
        self.forward_button.setStyleSheet(button_style)
        self.forward_button.clicked.connect(self.go_forward)
        self.toolbar.addWidget(self.forward_button)

        # Botão "Home"
        self.home_button = QPushButton("Home")
        self.home_button.setStyleSheet(button_style)
        self.home_button.clicked.connect(self.go_home)
        self.toolbar.addWidget(self.home_button)

        # Botão "Recarregar"
        self.reload_button = QPushButton("Recarregar")
        self.reload_button.setStyleSheet(button_style)
        self.reload_button.clicked.connect(self.reload_page)
        self.toolbar.addWidget(self.reload_button)

        # Botão para adicionar nova aba
        self.add_tab_button = QPushButton("Aba Nova")
        self.add_tab_button.setStyleSheet(button_style)
        self.add_tab_button.clicked.connect(self.add_new_tab)
        self.toolbar.addWidget(self.add_tab_button)

        # Botão para fechar aba atual
        self.close_tab_button = QPushButton("Fechar")
        self.close_tab_button.setStyleSheet(button_style)
        self.close_tab_button.clicked.connect(self.close_current_tab)
        self.toolbar.addWidget(self.close_tab_button)

        # Adiciona botão para fechar aba
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

    def add_new_tab(self):
        new_tab = BrowserTab()
        self.tabs.addTab(new_tab, "Nova Aba")
        self.tabs.setCurrentWidget(new_tab)

    def close_current_tab(self, index=None):
        if self.tabs.count() > 1:
            if index is None:
                index = self.tabs.currentIndex()
            self.tabs.removeTab(index)

    def go_back(self):
        current_tab = self.tabs.currentWidget()
        if current_tab and current_tab.browser.history().canGoBack():
            current_tab.browser.back()

    def go_forward(self):
        current_tab = self.tabs.currentWidget()
        if current_tab and current_tab.browser.history().canGoForward():
            current_tab.browser.forward()

    def go_home(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.browser.setUrl(QUrl("http://www.google.com"))  # Defina sua URL inicial aqui

    def reload_page(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.browser.reload()

    def navigate_to_url(self):
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, BrowserTab):
            url = self.search_bar.text()
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'http://' + url
            current_tab.browser.setUrl(QUrl(url))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())