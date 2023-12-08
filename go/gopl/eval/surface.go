// Surface computes an SVG rendering of a 3-D surface function.
package main

import (
	"fmt"
	"log"
	"math"
	"net/http"
)

const (
	width, height = 600, 320            // canvas size in pixels
	cells         = 100                 // number of grid cells
	xyrange       = 30.0                // axis ranges (-xyrange..+xyrange)
	xyscale       = width / 2 / xyrange // pixels per x or y unit
	zscale        = height * 0.4        // pixels per z unit
	angle         = math.Pi / 6         // angle of x, y axes (=30°)
)

var sin30, cos30 = math.Sin(angle), math.Cos(angle) // sin(30°), cos(30°)

func corner(i, j int, fn func(x, y float64) float64) (float64, float64) {
	// Find point (x,y) at corner of cell (i,j).
	x := xyrange * (float64(i)/cells - 0.5)
	y := xyrange * (float64(j)/cells - 0.5)
	// Compute surface height z.
	z := fn(x, y)
	// Project (x,y,z) isometrically onto 2-D SVG canvas (sx,sy).
	sx := width/2 + (x-y)*cos30*xyscale
	sy := height/2 + (x+y)*sin30*xyscale - z*zscale
	return sx, sy
}

func f(x, y float64) float64 {
	r := math.Hypot(x, y) // distance from (0,0)
	result := math.Sin(r) / r
	if math.IsInf(result, 0) {
		return math.MaxFloat64
	}
	return result
}

func parseAndCheck(s string) (Expr, error) {
	if s == "" {
		return nil, fmt.Errorf("empty expression")
	}
	expr, err := Parse(s)
	fmt.Println(expr)
	if err != nil {
		return nil, err
	}
	vars := make(map[Var]bool)
	if err := expr.Check(vars); err != nil {
		return nil, err
	}
	for v := range vars {
		if v != "x" && v != "y" && v != "r" {
			return nil, fmt.Errorf("undefined variable: %s", v)
		}
	}
	return expr, nil
}

func plot(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	expr, err := parseAndCheck(r.Form.Get("expr"))
	if err != nil {
		http.Error(w, "bad expr: "+err.Error(), http.StatusBadRequest)
		return
	}
	w.Header().Set("Content-Type", "image/svg+xml")
	surface(w, func(x, y float64) float64 {
		r := math.Hypot(x, y) // distance from (0,0)
		return expr.Eval(Env{"x": x, "y": y, "r": r})
	})
}

func surface(w http.ResponseWriter, fn func(x, y float64) float64) {
	fmt.Fprintf(w, "<svg xmlns='http://www.w3.org/2000/svg' "+
		"style='stroke: grey; fill: white; stroke-width: 0.7' "+
		"width='%d' height='%d'>", width, height)
	for i := 0; i < cells; i++ {
		for j := 0; j < cells; j++ {
			ax, ay := corner(i+1, j, fn)
			bx, by := corner(i, j, fn)
			cx, cy := corner(i, j+1, fn)
			dx, dy := corner(i+1, j+1, fn)
			fmt.Fprintf(w, "<polygon points='%g,%g %g,%g %g,%g %g,%g'/>\n",
				ax, ay, bx, by, cx, cy, dx, dy)
		}
	}
	fmt.Fprintf(w, "</svg>")
}

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		plot(w, r)
	})
	log.Fatal(http.ListenAndServe(":8080", nil))
}

//func main() {
//	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
//		w.Header().Set("Content-Type", "image/svg+xml")
//		fmt.Fprintf(w, "<svg xmlns='http://www.w3.org/2000/svg' "+
//			"style='stroke: #ff0000; fill: #0000ff; stroke-width: 0.7' "+
//			"width='%d' height='%d'>", width, height)
//		for i := 0; i < cells; i++ {
//			for j := 0; j < cells; j++ {
//				ax, ay := corner(i+1, j)
//				bx, by := corner(i, j)
//				cx, cy := corner(i, j+1)
//				dx, dy := corner(i+1, j+1)
//				fmt.Fprintf(w, "<polygon points='%g,%g %g,%g %g,%g %g,%g'/>\n",
//					ax, ay, bx, by, cx, cy, dx, dy)
//			}
//		}
//		fmt.Fprintf(w, "</svg>")
//	})
//	log.Fatal(http.ListenAndServe(":8080", nil))
//}
