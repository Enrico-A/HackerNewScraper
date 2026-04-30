import threading
import tkinter as tk
from tkinter import messagebox

from scraper import HackerNewsScraper


WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300


class HackerNewsScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hacker News Scraper 1.0 beta")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        self.status_var = tk.StringVar(value="Pronto")

        self._build_interface()

    def _build_interface(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", padx=40, pady=30)

        button_frame = tk.Frame(main_frame)
        button_frame.pack(expand=True)

        self.scrape_button = tk.Button(
            button_frame,
            text="Scrape Hacker News",
            command=self.start_scraping,
            width=22,
            height=2,
            font=("Arial", 12),
        )
        self.scrape_button.pack(pady=10)

        self.plot_button = tk.Button(
            button_frame,
            text="Plot Scores",
            command=self.plot_scores,
            width=22,
            height=2,
            font=("Arial", 12),
        )
        self.plot_button.pack(pady=10)

        status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            anchor="center",
            font=("Arial", 10),
        )
        status_label.pack(side="bottom", fill="x", pady=10)

    def start_scraping(self):
        self.status_var.set("Scraping in corso...")
        self.scrape_button.config(state="disabled")

        scraping_thread = threading.Thread(target=self._run_scraper, daemon=True)
        scraping_thread.start()

    def _run_scraper(self):
        try:
            scraper = HackerNewsScraper()
            scraper.run()
        except Exception as exc:
            self.root.after(0, self._show_error, "Errore scraping", str(exc))
        else:
            self.root.after(0, self.status_var.set, "Scraping completato")
        finally:
            self.root.after(0, self.scrape_button.config, {"state": "normal"})

    def plot_scores(self):
        try:
            import analytics

            analytics.main()
        except Exception as exc:
            self._show_error("Errore grafico", str(exc))
        else:
            self.status_var.set("Grafico generato")

    def _show_error(self, title, message):
        self.status_var.set("Pronto")
        messagebox.showerror(title, message)


def main():
    root = tk.Tk()
    HackerNewsScraperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
