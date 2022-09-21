# Overview

The vision of this project was to play with objects moving between the screens of Leeds to play with connecting the physically separated screens with movement and negative space. This was visualized through the concept of displaying clouds floating across the a night sky. Some artistic decisions made along the way involved the construction and movement of the clouds, stars, and the moon. 

### Construction

Each cloud is made up of circles. The number, size, and placement of the circles are all randomly varied. By playing around with parameters, I decided on a higher number of circles with lower opacity to “blur” the edges of each cloud. The main constraint here was the processing power of the machine. I had to balance the maximum number of circles per cloud based on how much the machine could handle before lagging the animation.

I chose to create two types of stars — a four-pointed star and a smaller plain circle. The four-pointed star was constructed using beginShape() function and geometrically calculating each vertex coordinate. The two colors were chosen to create more interesting variety in the sky background.

The moon is the simplest element in terms of shape construction. It has fixed position with craters that change position each time the script is run. The craters were calculated to never overlap with the moon’s edge so that the moon would appear as one cohesive unit.

### Movement

The clouds moving across the screens is the most important motion in the piece. The speed at which a cloud moves varies from cloud to cloud, which introduces a sense of depth where the faster clouds appear closer. The clouds also have a small y-dimension movement in order to help the clouds appear like they’re floating in air. This movement was created using a sine wave. In order to accentuate this floating movement, each circle within a cloud has a different offset so that they don’t all sway at the same time. The aim here was to make the movement of clouds look as organic as possible.

The stars in the background also introduce movement in the piece by twinkling at different rates. The twinkling effect was created by increasing then decreasing the opacity of a star. This was calculated using modulo, where each star has a different modulo for determining the rate of twinkle. I also chose to have each star also appear in a different location after each twinkle to contrast with the static moon.

### Mapping onto Leeds

Altering my original script to fit the Leeds projector mapping was probably the most technically difficult part of the project. The moon and stars had no issue with the mapping because they did not have to interact between screens. The most glaring issue was the 90-degree clockwise rotation of the projector screens. I originally coded the script to move horizontally across my computer screen, meaning they would be moving vertically on the Leeds screens. The simple solution to this was to exchange the x-position and y-position variables when moving each circle within a cloud.

The next issue I had to face was getting the clouds to enter the next screen after leaving the first. This was done by recalculating the y-position of each cloud after leaving a screen so that it would enter at the its respective position in the next screen. This was semi-hard coded as I had to pick out how many screen-lengths the y-position had to skip to in order to move to the next screen.

I also encountered the issue of fullscreening the two extended displays. I ended up solving this by fullscreening all three displays using fullScreen(SPAN) and accounting for the x-dimension offset of the main display. It’s definitely not the most elegant solution but it works.

### Generalization
In order to generalize this to a normal non-rotated, non-Leeds display, the move() and display() functions under the cloud class must be altered:

Replace the entire <if(xpos[i] < -90)> statement under move() with:

    if(getXpos() < -90) {

    setCloud();
    
    }

Replace the <circle(ypos[i], xpos[i], size[i])> statement under display() with:

    circle(xpos[i], ypos[i], size[i]);