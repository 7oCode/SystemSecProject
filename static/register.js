var tl = new TimelineMax();

$('.card-number').focus(function(){
  tl.to('.credit-card-container', .2, { background: '#F9F9F9'})
    .to('.bg-circle-one', .2, { background: '#EEEEEE' }, '-=1')
    .to('.bg-circle-two', .2, { background: '#F3f3f3'}, '-=1')
    .to('.credit-card-number-container', .2, { background: '#79B2F9', border: '2px solid #0080FF' }, '-=1')
    .to('.name-container', .2, { background: 'transparent', border: '2px solid transparent' }, '-=1')
    .to('.date-container', .2, { background: 'transparent', border: '2px solid transparent' }, '-=1')

});

$('.first-name-input').focus(function(){
  tl.to('.credit-card-container', .2, { background: '#F9F9F9'})
    .to('.credit-card-number-container', .2, { background: 'transparent', border: '2px solid transparent'}, '-=1')
    .to('.bg-circle-one', .2, { background: '#EEEEEE' }, '-=1')
    .to('.bg-circle-two', .2, { background: '#F3f3f3'}, '-=1')
    .to('.name-container', .2, { background: '#79B2F9', border: '2px solid #0080FF' }, '-=1')
    .to('.date-container', .2, { background: 'transparent', border: '2px solid transparent' }, '-=1')
});

$('.exp-date-input').focus(function(){
  tl.to('.credit-card-container', .2, { background: '#F9F9F9'})
    .to('.credit-card-number-container', .2, { background: 'transparent', border: '2px solid transparent'}, '-=1')
    .to('.name-container', .2, { background: 'transparent', border: '2px solid transparent'}, '-=1')
    .to('.date-container', .2, { background: '#79B2F9', border: '2px solid #0080FF' }, '-=1')
    .to('.bg-circle-one', .2, { background: '#EEEEEE' }, '-=1')
    .to('.bg-circle-two', .2, { background: '#F3f3f3'}, '-=1')
    .to('.name-container', .2, { background: 'transparent', border: '2px solid transparent' }, '-=1')
    .to('.credit-card-number-container', .2, { background: 'transparent', border: '2px solid transparent' }, '-=1')
});

$('.cvv-input').focus(function(){
   // tl.to('.credit-card-number-container', 1,  { rotationY:'+=180'})
   console.log('test');
});

$('.add-card').click(function(){
  tl.to('.credit-card-container', .3, { y: 10  })
  tl.to('.credit-card-container', .3, { y: 0 })

    .to('.credit-card-container', .2, { background: '#0080FF'}, '-=1')
    .to('.bg-circle-one', .2, { background: 'linear-gradient(#006cd6, #0080FF)' }, '-=1')
    .to('.bg-circle-two', .2, { background: 'linear-gradient(#006CD6, #0080FF)'}, '-=1')
    .to('.credit-card-number-container', .2, { background: 'transparent', border: '2px solid transparent' }, '-=1')
    .to('.name-container', .2, { background: 'transparent', border: '2px solid transparent' }, '-=1')
    .to('.date-container', .2, { background: 'transparent', border: '2px solid transparent' }, '-=1')
    .to('.card-animation', .5, { x: 600, opacity:0, display: 'none' })
    .to('.credit-card-loader-fill', .5, { width: '100%', background:'#0080FF' })
    .to('.credit-card-loader', .1, { alphaAuto: 1 })




});
