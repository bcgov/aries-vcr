# Accessibility

This applications aims to meet or exceed the [World Wide Web Consortium (W3C) Web Content Accessibility Guidelines (WCAG) 2.0](https://www.w3.org/TR/WCAG20/).

## Tested Assistive Technologies

The following technologies are recommended to be tested with this application, chosen because of their popularity and coverage using data from http://webaim.org/projects/screenreadersurvey6/:

1. JAWS IE 11 on Windows 10
2. NVDA Firefox (evergreen) on Windows 10 
3. VoiceOver on Mac OS (should get iOS coverage)

## General Advice

1. Use native HTML5 elements/attributes where possible, e.g., `<header><nav><label><input required>`
1. Do not just code it, test it yourself with a screen reader!
1. Establish your patterns early during development, less effort up-front than retro fitting later.

## Implementation Patterns

### Tab Indexing

1. Assign tabindex to "0" for controls that needs to be included in tab index.
1. Assign tabindex to "-1" for controls that needs to be excluded from tab index.

### Dynamically Displayed Content

Screen readers need to be notified when new content/forms are dynamically displayed:

1. (AngularJS) Avoid `[hidden]="expression"` use `*ngIf="expression"` instead.  Screen readers tend to read hidden elements.
1. For errors, announce revealed content with `role="alert" aria-live="assertive"`
1. If revealing new for element use  `role="dialogue"`
1. If you have multiple errors, wrap a `<div role="alert" aria-live="assertive">` around all the messages


### Radio Buttons or Group of fields with a single label 

1. Use `<label for="">` for the first radio control
1. Use a hidden label `<label class="visuallyhidden" for="">` for the second and so on controls
 
 ```
/*
  Special accessibility class to hide things like labels but still have the readable by screen readers
 */
.visuallyhidden {
  position: absolute;
  overflow: hidden;
  clip: rect(0 0 0 0);
  height: 1px; width: 1px;
  margin: -1px; padding: 0; border: 0;
}
```

