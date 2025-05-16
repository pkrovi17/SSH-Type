package main

import (
	"log"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/wish"
	wishtea "github.com/charmbracelet/wish/bubbletea"
)

type model struct{}

func (model) Init() tea.Cmd                             { return nil }
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) { return m, nil }
func (model) View() string {
	return "👋 Welcome to your SSH TUI!\nPress Ctrl+C to exit.\n"
}

func main() {
	tui := func() (tea.Model, tea.Cmd) {
		return model{}, nil
	}

	srv, err := wish.NewServer(
		wish.WithAddress(":2323"),
		wish.WithMiddleware(
			wishtea.Middleware(tui),
		),
	)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("✅ Server listening on port 2323...")
	if err := srv.ListenAndServe(); err != nil {
		log.Fatal(err)
	}
}
