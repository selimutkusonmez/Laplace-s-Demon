        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 15px; font-size: 32px; font-style: italic;">
                        &chi;<sup>2</sup> = &Sigma;
                    </td>
                    <td align="center">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor; padding: 0 10px 4px 10px; font-size: 26px;">
                                    (O &minus; E)<sup>2</sup>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 6px 10px 0 10px; font-size: 26px;">
                                    E
                                </td>
                            </tr>
                        </table>
                    </td>
                    <td valign="middle" style="padding-left: 20px; font-size: 30px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)

