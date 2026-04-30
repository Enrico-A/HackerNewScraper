import threading
import tkinter as tk
from tkinter import messagebox

from scraper import HackerNewsScraper


# Dimensioni fisse della finestra principale.
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300


class HackerNewsScraperApp:
    """Interfaccia Tkinter per avviare lo scraper e visualizzare il grafico."""

    def __init__(self, root):
        # Conserva il riferimento alla finestra e imposta titolo, dimensioni e resize.
        self.root = root
        self.root.title("Hacker News Scraper 1.0 beta")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        # Variabile reattiva usata dall'etichetta di stato in fondo alla finestra.
        self.status_var = tk.StringVar(value="Pronto")

        self._build_interface()

    def _build_interface(self):
        """Costruisce pulsanti e area di stato dell'applicazione."""
        # Frame principale con margini comodi per separare i controlli dal bordo.
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", padx=40, pady=30)

        # Frame dedicato ai pulsanti, centrato verticalmente nella finestra.
        button_frame = tk.Frame(main_frame)
        button_frame.pack(expand=True)

        # Pulsante che avvia lo scraping in background.
        self.scrape_button = tk.Button(
            button_frame,
            text="Scrape Hacker News",
            command=self.start_scraping,
            width=22,
            height=2,
            font=("Arial", 12),
        )
        self.scrape_button.pack(pady=10)

        # Pulsante che apre il grafico dei punteggi salvati nel database.
        self.plot_button = tk.Button(
            button_frame,
            text="Plot Scores",
            command=self.plot_scores,
            width=22,
            height=2,
            font=("Arial", 12),
        )
        self.plot_button.pack(pady=10)

        # Etichetta sempre visibile per comunicare stato, errori e completamento.
        status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            anchor="center",
            font=("Arial", 10),
        )
        status_label.pack(side="bottom", fill="x", pady=10)

    def start_scraping(self):
        """Disabilita il pulsante e avvia lo scraper su un thread separato."""
        self.status_var.set("Scraping in corso...")
        self.scrape_button.config(state="disabled")

        # Il thread evita che la GUI si blocchi mentre vengono scaricate le pagine.
        scraping_thread = threading.Thread(target=self._run_scraper, daemon=True)
        scraping_thread.start()

    def _run_scraper(self):
        """Esegue lo scraper e aggiorna la GUI in modo thread-safe."""
        try:
            scraper = HackerNewsScraper()
            scraper.run()
        except Exception as exc:
            # root.after rimanda l'aggiornamento al thread principale di Tkinter.
            self.root.after(0, self._show_error, "Errore scraping", str(exc))
        else:
            self.root.after(0, self.status_var.set, "Scraping completato")
        finally:
            # Riabilita sempre il pulsante, anche quando lo scraping fallisce.
            self.root.after(0, self.scrape_button.config, {"state": "normal"})

    def plot_scores(self):
        """Importa il modulo di analytics e genera il grafico dei punteggi."""
        try:
            # Import locale: matplotlib viene caricato solo quando serve davvero.
            import analytics

            analytics.main()
        except Exception as exc:
            self._show_error("Errore grafico", str(exc))
        else:
            self.status_var.set("Grafico generato")

    def _show_error(self, title, message):
        """Mostra una finestra di errore e riporta lo stato dell'app a 'Pronto'."""
        self.status_var.set("Pronto")
        messagebox.showerror(title, message)


def main():
    """Crea la finestra Tkinter e avvia il loop grafico."""
    root = tk.Tk()
    HackerNewsScraperApp(root)
    root.mainloop()


if __name__ == "__main__":
    # Permette di lanciare la GUI direttamente con: python app.py
    main()
