include <variables.scad>

use <batteryBox.scad>
use <pcb.scad>
use <pcbBox.scad>
use <pcbTopBox.scad>
use <pcbBottomBox.scad>


// explode(5, false);
// HoledBox(50, 20, 10, holeRadius, holeRadius*2, true);
// pcbBox();
// pcbBottomBox();
pcbTopBox();
// batteryBoxV2();

module Text(string, position) {
	translate(position)
	translate([3,0,0])
	rotate([90, 0, 0])
	text(string, size=5, valign="center");

	translate(position)
	color("Red")
	cube(1, center=true);
}

module explode(distance, cut) {

	color(alpha=1)
	difference() {
		union() {
			translate([0, 0, -distance*2]) {
				translate([-PCBNotchWidth, 0, -(stickRadius+PCBToTopSpacing+PCBComponentsHeight)])
				PCB();
				pcbBottomBox();
			}

			translate([0, 0, -distance*1])
			pcbTopBox();

			scale([1.1, 0.999, 0.999])
			rotate([0, 90, 0])
			cylinder(MaxLength, r=stickRadius, center=true, $fn=40);

			translate([0, 0, distance*1])
			rotate([180, 0, 0])
			batteryBoxV2();
		}
		if(cut) {
			color("White",alpha=1)
			translate([-50, -105, -500])
			cube([100,100,1000]);
		}
	}
}
