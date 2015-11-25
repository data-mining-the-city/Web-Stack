var boxMullerRandom = (function () {
    var phase = 0,
        RAND_MAX,
        array,
        random,
        x1, x2, w, z;

    if (crypto && typeof crypto.getRandomValues === 'function') {
        RAND_MAX = Math.pow(2, 32) - 1;
        array = new Uint32Array(1);
        random = function () {
            crypto.getRandomValues(array);

            return array[0] / RAND_MAX;
        };
    } else {
        random = Math.random;
    }

    return function () {
        if (!phase) {
            do {
                x1 = 2.0 * random() - 1.0;
                x2 = 2.0 * random() - 1.0;
                w = x1 * x1 + x2 * x2;
            } while (w >= 1.0);

            w = Math.sqrt((-2.0 * Math.log(w)) / w);
            z = x1 * w;
        } else {
            z = x2 * w;
        }

        phase ^= 1;

        return (z);
    }
}());

function randomWalk(steps, randFunc) {
    steps = steps >>> 0 || 100;
    if (typeof randFunc !== 'function') {
        randFunc = boxMullerRandom;
    }

    var points = [],
        value = 3,
        t;

    for (t = 0; t < steps; t += 1) {
        value += randFunc();
        points.push(Math.abs(value));
    }

    return points;
}

