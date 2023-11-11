import {
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React from "react"

// The library does not provide @types
const reveal = require('react-reveal');

interface State {
  numClicks: number
  isFocused: boolean
}

class FrontPageComponent extends StreamlitComponentBase<State> {
  public state = { numClicks: 0, isFocused: false }

  public render = (): JSX.Element => {
    const { theme } = this.props
    let images = this.props.args["images"];
    var origin = (window.location != window.parent.location)
            ? document.referrer
            : document.location.href; 

    const cardStyle: any = {
      width: '100%',
      minHeight: '10vw',
      borderRadius: '4vw',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      marginTop: '1vw',
      marginBottom: '1vw',
      flexDirection: 'column',
    };

    const containerStyle: any = {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr 1fr',
      gridGap: '20px',
    };

    const textColumnStyle: any = {
      gridColumn: '1 / 2', // Span the first column
    };

    const imageColumnStyle: any = {
      display: 'flex',
      flexDirection: 'column',
    };

    const imageStyle: any = {
      width: '100%',
      marginBottom: '20px',
      borderRadius: '2vw',
    };

    const dividerStyle: any = {
      width: '100%',
      borderTop: theme ? `0.125rem solid ${theme.primaryColor}` : '0.125rem solid #000',
      margin: '10px 0',
    };

    return (
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        <reveal.Fade right big delay={100}>
          <div style={cardStyle}>
            <h1> Pomorski Czarodziej 🧙‍♂️ </h1>
          </div>
        </reveal.Fade>

        <reveal.Fade right big cascade delay={200}>
          <div style={dividerStyle}></div>
        </reveal.Fade>

        <reveal.Fade right big delay={1000}>
          <div style={cardStyle}>
            <h2> Cel konkursu </h2>
            <p style={{}}>
              Celem jaki przyświeca nam przy organizacji tego konkursu jest rozwijanie zainteresowań algorytmiką i technologią informatyczną. Zależ nam na popularyzowaniu programowania w klasach szkół podstawowych.
              Odpowiadamy na propozycję zmian w podstawie programowej wprowadzającą elementy programowania od najmłodszych lat.
              Konkurs ma sprzyjać rozwojowi uzdolnień i zainteresowań, pobudzać do twórczego myślenia, wspomagać zdolności stosowania zdobytej wiedzy w praktyce oraz docelowo przyczynić się do lepszego przygotowania uczniów do nauki w szkołach wyższego stopnia.
              Chcemy pokazać, że używając powszechnie bardzo popularnego języka programowania jakim jest Python, można zaszczepiać koncepty programistyczne już w szkole podstawowej.
              Konkurs jest darmowy. Udział mogą wziąć wszystkie szkoły prywatne i publiczne z województwa pomorskiego.
            </p>
          </div>
        </reveal.Fade>

        <reveal.Fade right big cascade delay={1100}>
          <div style={dividerStyle}></div>
        </reveal.Fade>

        <reveal.Fade right big delay={2000}>
          <div style={cardStyle}>
            <div style={containerStyle}>
              <div style={textColumnStyle}>
                <h2>Historia konkursu</h2>
                <p style={{}}>
                  Konkurs programowania dla szkół podstawowych organizujemy wspólnie z nauczycielami od 2010 roku. W pierwszej, kameralnej edycji uczestniczyły jedynie 4 szkoły.
                  Na przestrzeni lat konkurs zyskiwał coraz większą popularności i bywało, że udział brała nawet ponad setka dzieci z prawie dwudziestu pomorskich szkół.
                  Podczas poprzednich edycji aktywnie współpracowaliśmy z Kuratorium Oświaty w Gdańsku. Od 2022 zmieniamy formułę konkursu, wychodząc naprzeciw nowym trendom na rynku i zmianą programowym.
                  Stosowany do tej pory Baltiee zastępujemy językiem Python.
                </p>
                <p style={{}}>
                  Już tradycją stało się, że gala finałowa konkursu oraz wręczenie nagród odbywa się w siedzibie firmy Intel Technology Poland, gdzie pokazujemy, jak wygląda praca programisty komputerowego,
                  oprowadzamy uczestników po biurze oraz przeprowadzamy krótkie lekcje związane z technologią informacyjną.
                </p>
              </div>
              <div style={imageColumnStyle}>
                <reveal.Fade right cascade>
                <img src={origin + images[0]} alt="Image 1" style={imageStyle} />
                <img src={origin + images[1]} alt="Image 2" style={imageStyle} />
                <img src={origin + images[2]} alt="Image 3" style={imageStyle} />
                </reveal.Fade>
              </div>
              <div style={imageColumnStyle}>
                <reveal.Fade right cascade>
                  <img src={origin + images[3]} alt="Image 4" style={imageStyle} />
                  <img src={origin + images[4]} alt="Image 5" style={imageStyle} />
                  <img src={origin + images[5]} alt="Image 6" style={imageStyle} />
                </reveal.Fade>
              </div>
            </div>
          </div>
        </reveal.Fade>

        <reveal.Fade right big cascade delay={2100}>
          <div style={dividerStyle}></div>
        </reveal.Fade>
      </div>
    )
  }
}

export default withStreamlitConnection(FrontPageComponent)
